#! /srv/homeassistant/bin/python3

"""switchmate.py

A python-based command line utility for controlling Switchmate switches

Usage:
    ./switchmate.py scan
    ./switchmate.py status [<mac_address>]
    ./switchmate.py <mac_address> auth
    ./switchmate.py <mac_address> <auth_key> switch [on | off]
    ./switchmate.py -h | --help
"""

from __future__ import print_function
import struct
import sys
import ctypes
import functools
from binascii import hexlify, unhexlify

from bluepy.btle import Scanner, DefaultDelegate, Peripheral, ADDR_TYPE_RANDOM, BTLEException
import appdaemon.plugins.hass.hassapi as hass

SWITCHMATE_SERVICE = '23d1bcea5f782315deef121223150000'
NOTIFY_VALUE = struct.pack('<BB', 0x01, 0x00)

AUTH_NOTIFY_HANDLE = 0x0017
AUTH_HANDLE = 0x0016
AUTH_INIT_VALUE = struct.pack('<BBBBBB', 0x00, 0x00, 0x00, 0x00, 0x01, 0x00)

STATE_HANDLE = 0x000e
STATE_NOTIFY_HANDLE = 0x000f

def c_mul(a, b):
    '''
    Multiplication function with overflow
    '''
    return ctypes.c_int64((a * b) &0xffffffffffffffff).value

def sign(data, key):
    '''
    Variant of the Fowler-Noll-Vo (FNV) hash function
    '''
    blob = data + key
    x = blob[0] << 7
    for c in blob:
        x1 = c_mul(1000003, x)
        x = x1 ^ c ^ len(blob)

    # once we have the hash, we append the data
    shifted_hash = (x & 0xffffffff) << 16
    shifted_data_0 = data[0] << 48
    shifted_data_1 = data[1] << 56
    packed = struct.pack('<Q', shifted_hash | shifted_data_0 | shifted_data_1)[2:]
    return packed

class NotificationDelegate(DefaultDelegate):
    def __init__(self, appdaemonAPI):
        DefaultDelegate.__init__(self)
        self.retry_count = 0
        self.retry_max = 0
        self.retry_method = None
        self.entity = None
        self.target_state = None
        self.apiHandler = appdaemonAPI

    def setRetryParams(self, retry_max, retry_method):
        self.retry_max = retry_max
        self.retry_method = retry_method

    def setToggleEntity(self, entity):
        self.entity = entity

    def setTargetState(self, state):
        self.target_state = state

    def handleNotification(self, handle, data):
        if handle == AUTH_HANDLE:
            self.apiHandler.log('Auth key is {}'.format(hexlify(data[3:]).upper()))
        else:
            if data[-1] == 0:
                self.apiHandler.log("Switched successfully")
                self.apiHandler.set_state(self.entity, state=self.target_state)
            else:
                self.apiHandler.log("Switch failed")

                if self.retry_count < self.retry_max:
                    self.retry_count += 1
                    self.apiHandler.log("Retry number {}".format(self.retry_count))

                    self.retry_method()

class ScanDelegate(DefaultDelegate):
    def __init__(self, mac_address):
        DefaultDelegate.__init__(self)
        self.mac_address = mac_address
        self.seen = []

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if self.mac_address != None and self.mac_address != dev.addr:
            return

        if dev.addr in self.seen:
            return
        self.seen.append(dev.addr)

        AD_TYPE_UUID = 0x07
        AD_TYPE_SERVICE_DATA = 0x16
        if dev.getValueText(AD_TYPE_UUID) == SWITCHMATE_SERVICE:
            data = dev.getValueText(AD_TYPE_SERVICE_DATA)
            # the bit at 0x0100 signifies if the switch is off or on
            exit_code = (1, 0)[(int(data, 16) >> 8) & 1]
            if exit_code == 1:
                print('off')
            else:
                print('on')

class SwitchmateSwitch(object):
    def __init__(self, name, mac, auth):
        self.name = name
        self.mac = mac
        self.auth = auth


class SwitchmateSwitcher(hass.Hass):
    def __init__(self, ad, name, logger, error, args, config, app_config, global_vars):
        super().__init__(ad, name, logger, error, args, config, app_config, global_vars)
        self.switchmate_config = None
        self.switches = {}

    def initialize(self):
        self.switchmate_config = self.args['switches']
        self.log("Loaded switchmate config: {}".format(self.switchmate_config))
        for name, config in self.switchmate_config.items():
            self.switches[name] = SwitchmateSwitch(name, config.get('mac'), config.get('auth'))
            self.listen_event(self.on_switchmate_command, name)

    def on_switchmate_command(self, event, data, kwargs):
        notifications = NotificationDelegate(self)
        switch = self.switches.get(event)
        if switch is None:
            return

        command = data.get('command')
        on = data.get('is_on')

        if command == "status" and switch.mac is not None:
            self.status_command(switch.mac)
        elif command == "scan":
            self.scan_command()
        elif command == "switch" and switch.mac is not None and switch.auth is not None:
            device = self.connect(switch.mac)
            if device is None:
                return

            if command == "switch":
                auth_key = unhexlify(switch.auth)
                switch_method = functools.partial(self.switch_command, device, auth_key, on)
                notifications.setRetryParams(5, switch_method)
                notifications.setToggleEntity(".".join(["input_boolean", switch.name]))
                notifications.setTargetState("on" if on else "off")

            device.setDelegate(notifications)

            switch_method()

            self.log('Waiting for response')
            for _ in range(10):
                if device.waitForNotifications(1.0):
                    break

            device.disconnect()

    def status_command(self, mac_address):
        self.log('Looking for switchmate status...')
        sys.stdout.flush()

        scanner = Scanner().withDelegate(ScanDelegate(mac_address))

        scanner.clear()
        scanner.start()
        scanner.process(20)
        scanner.stop()

    def scan_command(self):
        self.log('Scanning...')
        sys.stdout.flush()

        scanner = Scanner()
        devices = scanner.scan(10.0)

        SERVICES_AD_TYPE = 7

        switchmates = []
        for dev in devices:
            for (adtype, desc, value) in dev.getScanData():
                is_switchmate = adtype == SERVICES_AD_TYPE and value == SWITCHMATE_SERVICE
                if is_switchmate and dev not in switchmates:
                    switchmates.append(dev)

        if len(switchmates):
            self.log('Found Switchmates:')
            for switchmate in switchmates:
                self.log(switchmate.addr)
        else:
            self.log('No Switchmate devices found');

    def connect(self, mac, retries=5):
        device = None
        attempts = 0
        while device is None and attempts < retries:
            try:
                device = Peripheral(mac, ADDR_TYPE_RANDOM)
            except BTLEException:
                attempts += 1
                self.log("Attempting to connect count = {}".format(attempts))

        return device

    def switch_command(self, device, auth_key, on):
        val = None
        device.writeCharacteristic(STATE_NOTIFY_HANDLE, NOTIFY_VALUE, True)
        if on:
            val = b'\x01\x01'
        else:
            val = b'\x01\x00'
        device.writeCharacteristic(STATE_HANDLE, sign(val, auth_key))
