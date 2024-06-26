import event_dispatcher
import state_machine
from util import logger
from util import hassutil
from events.presence_event import PresenceEvent
from actions.push_notify_action import PushNotifyAction
from actions.light_action import LightAction
from actions.thermostat_action import ThermostatAction
from actions.door_lock_action import DoorLockAction
from actions.switch_action import SwitchAction

def register_callbacks():
    event_dispatcher.register_callback(on_presence_changed, PresenceEvent.__name__)
    
def on_presence_changed(event):
    if event.new == "not_home":
        on_person_away(event.name)
    elif event.new == "home":
        on_person_home(event.name)

def on_person_away(name):
    logger.info("{} has left home".format(name))
    
    if hassutil.is_nobody_home():
        handle_nobody_home()
    
    if name == "Jim Presence":
        DoorLockAction().add_lock("Front Entrance Lock").lock()

        if state_machine.is_garage_open():
            PushNotifyAction().add_target("jim_cell").set_message("Garage door is open!", notification_id="garage-alert", tts=True).notify()


def on_person_home(name):
    logger.info("{} has arrived home".format(name))
    
    handle_somebody_home()
        
def handle_nobody_home():
    logger.info("Nobody home...")

    if not state_machine.is_enabled("Guest Mode"):
        hassutil.activate_scene("Nobody Home")

        if state_machine.is_heating_enabled():
            heat_action = ThermostatAction().add_thermostat("Oil Thermostat")
            heat_action.set_temperature(state_machine.get_number("Away Heat"), 'heat')

        if state_machine.is_enabled("Christmas Lights Mode"):
            LightAction().add_light("Christmas Tree LEDs").turn_off()
            SwitchAction().add_switches([
                "Smart Strip Outlet 1",
                "Smart Strip Outlet 2",
                "Smart Strip Outlet 3",
                "Smart Strip Outlet 4"
            ]).turn_off()
        
        #TODO: schedule timer for simulating someone being home
    
def handle_somebody_home():
    logger.info("Someone is home now...")
    
    LightAction().add_lights(["Kitchen Lights", "Kitchen Cabinet Lights", "Dining Room Light", "Living Room Lamps"]).turn_on()

    if state_machine.is_heating_enabled():
        heat_action = ThermostatAction().add_thermostat("Oil Thermostat")
        heat_action.set_temperature(state_machine.get_number("Normal Heat"), 'heat')

    if state_machine.is_enabled("Christmas Lights Mode") and not state_machine.is_enabled("Sleep Mode"):
            LightAction().add_light("Christmas Tree Lights").turn_on_no_brightness()
            SwitchAction().add_switches([
                "Smart Strip Outlet 1",
                "Smart Strip Outlet 2",
                "Smart Strip Outlet 3",
                "Smart Strip Outlet 4"
            ]).turn_on()
    
    #TODO: cancel timer for simulating someone being home
    #TODO: set lights / thermostats / tvs