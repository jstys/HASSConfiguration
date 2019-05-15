#!/srv/homeassistant/bin/python3
import os
import importlib
import re
import sys

from util import hassutil
from util import entity_map
from util.entity_map import entity_map
from util import logger
from events.sunrise_event import SunriseEvent
from events.sunset_event import SunsetEvent
import appdaemon.plugins.hass.hassapi as hass
import event_factory
import event_dispatcher
import state_machine
import timer_manager

class AutomationHub(hass.Hass):
    def initialize(self):
        hassutil.set_api_handle(self)
        timer_manager.set_api_handle(self)
        self.event_list = self.args["event_list"]
        self.setup_logger()
        self.subscribe_events()
        self.subscribe_states()
        if not hasattr(self, "event_handler_map"):
            self.event_handler_map = {}
        self._load_handlers()
        self._initialize_states()
        
    def _load_handlers(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        handler_path = os.path.join(cwd, "event_handlers")
        ls_output = os.listdir(handler_path)
        module_files = [pyfile.replace('.py', '') for pyfile in ls_output if re.match(r'^.+\.py$', pyfile) and '__init__.py' not in pyfile]
        
        event_dispatcher.clear_callbacks()
        
        for module_name in module_files:
            if module_name in self.event_handler_map:
                module = importlib.reload(self.event_handler_map[module_name])
            else:
                module = importlib.import_module(".".join(["event_handlers", module_name]))
            module.register_callbacks()
            self.event_handler_map[module_name] = module
        
    def _initialize_callbacks(self):
        self.run_at_sunrise(self.on_sunrise)
        self.run_at_sunset(self.on_sunset)
        
    def _initialize_states(self):
        # Get HASS States
        sleep_state = self.get_state(entity="input_boolean.sleep_mode", namespace="hass") == "on"
        thermostat_mode = self.get_state(entity="input_select.thermostat_mode", namespace="hass")
        sunup_state = self.get_state(entity="sun.sun", namespace="hass") == "above_horizon"
        
        # Add try/except around appdaemon methods which may fail
        try:
            nobody_home = self.noone_home(namespace="hass")
        except:
            nobody_home = False
        
        state_machine.set_state(state_machine.SUN_UP_STATE, sunup_state)
        state_machine.set_state(state_machine.SLEEP_STATE, sleep_state)
        state_machine.set_state(state_machine.THERMOSTAT_STATE, thermostat_mode)
        state_machine.set_state(state_machine.NOBODY_HOME_STATE, nobody_home)
    
    def setup_logger(self):
        log = self.get_main_log()
        logger.set_logger(log)
    
    def subscribe_events(self):
        self.listen_event(self.on_event, namespace="global")
        
    def on_event(self, event_name, data, kwargs):
        logger.info("Received New Event - name = {} data = {} kwargs = {}".format(event_name, data, kwargs))

        if event_name in self.event_list:
            logger.info("Received subscribed event")
            
            adevent = event_factory.create_from_event(event_name, data, kwargs)
            if adevent:
                event_dispatcher.dispatch(adevent)
        
    def subscribe_states(self):
        self.listen_state(self.on_state_changed, attribute="all", namespace="global")
        
    def on_state_changed(self, entity, attribute, old, new, kwargs):
        
        if entity in entity_map:
            logger.info("Received New State Change - entity = {} attribute = {} old = {} new = {} kwargs = {}".format(entity, attribute, old, new, kwargs))
            logger.info("Received state change for subscribed entity (name = {}, type = {}".format(entity_map[entity]['name'], entity_map[entity]['type']))
            
            friendly_name = entity_map[entity]["name"]
            entity_type = entity_map[entity]["type"]
            old_state = old.get("state") if old else None
            new_state = new.get("state") if new else None
            attributes = new.get("attributes")
            
            adevent = event_factory.create_from_state_change(friendly_name, entity_type, entity, attributes, old_state, new_state, kwargs)
            if adevent:
                event_dispatcher.dispatch(adevent)
                
    def timer_callback(self, kwargs):
        partial = kwargs.get("partial")
        name = kwargs.get("title")
        if partial:
            partial()
        timer_manager.remove_timer(name)