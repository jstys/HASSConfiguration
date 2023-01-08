import event_dispatcher
import state_machine
from util import logger
from util import hassutil
from events.input_event import InputEvent
from actions.light_action import LightAction
from actions.join_action import JoinAction
from actions.thermostat_action import ThermostatAction
from actions.switch_action import SwitchAction

def event_filter(event):
    return event.name == "sleep_mode"

def register_callbacks():
    event_dispatcher.register_callback(on_state_changed, InputEvent.__name__, event_filter=event_filter)
    
def on_state_changed(event):
    if event.new == "off":
        on_sleep_state_disabled(event)
    elif event.new == "on":
        on_sleep_state_enabled(event)
    else:
        logger.warning("Invalid state transition for sleep state")

def on_sleep_state_enabled(event):
    logger.info("Sleep state enabled")
    hassutil.activate_scene("sleep_mode")

    if state_machine.is_jim_home():
        JoinAction().add_target("jim_cell").send_taker_command("bed_command")

    if state_machine.is_heating_enabled():
        heat_action = ThermostatAction().add_thermostat("oil_thermostat")
        heat_action.set_temperature(state_machine.get_number("sleep_mode_heat"), 'heat')

    if state_machine.is_enabled("christmas_lights_mode"):
        LightAction().add_light("christmas_tree_lights").turn_off()

def on_sleep_state_disabled(event):
    logger.info("Sleep state disabled")
    
    SwitchAction().add_switch("master_bedroom_whitenoise").turn_off()
    LightAction().add_lights(["first_floor_staircase_led"]).turn_off()
    ThermostatAction().add_thermostat("master_bedroom_minisplit").turn_off()

    if state_machine.is_jim_home():
        JoinAction().add_target("jim_cell").send_taker_command("awake_command")

    if state_machine.is_heating_enabled():
        heat_action = ThermostatAction().add_thermostat("oil_thermostat")
        heat_action.set_temperature(state_machine.get_number("normal_heat"), 'heat')

    if state_machine.is_enabled("christmas_lights_mode"):
        LightAction().add_light("christmas_tree_lights").turn_on_no_brightness()
        SwitchAction().add_switches([
            "aeon_labs_smart_strip_1",
            "aeon_labs_smart_strip_2",
            "aeon_labs_smart_strip_3",
            "aeon_labs_smart_strip_4"
        ]).turn_off()
    