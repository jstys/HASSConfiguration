import event_dispatcher
import state_machine
from util import logger
from events.input_event import InputEvent
from actions.light_action import LightAction
from actions.thermostat_action import ThermostatAction
from actions.switch_action import SwitchAction

def event_filter(event):
    return event.name == "vacation_mode"

def register_callbacks():
    event_dispatcher.register_callback(on_state_changed, InputEvent.__name__, event_filter=event_filter)
    
def on_state_changed(event):
    if event.new == "off":
        on_disabled(event)
    elif event.new == "on":
        on_enabled(event)
    else:
        logger.warning("Invalid state transition for vacation mode")

def on_enabled(event):
    if state_machine.is_heating_enabled():
        ThermostatAction().add_thermostat("oil_thermostat").set_temperature(state_machine.get_number("vacation_heat"), "heat")

    if state_machine.is_enabled("christmas_lights_mode"):
        LightAction().add_light("christmas_tree_lights").turn_off()
        SwitchAction().add_switches([
            "aeon_labs_smart_strip_1",
            "aeon_labs_smart_strip_2",
            "aeon_labs_smart_strip_3",
            "aeon_labs_smart_strip_4"
        ]).turn_off()

def on_disabled(event):
    if state_machine.is_heating_enabled():
        ThermostatAction().add_thermostat("oil_thermostat").set_temperature(state_machine.get_number("normal_heat"), "heat")