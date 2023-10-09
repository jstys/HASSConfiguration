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
        heat_action = ThermostatAction().add_thermostat("Oil Thermostat")
        heat_action.set_temperature(state_machine.get_number("sleep_mode_heat"), 'heat')

    if state_machine.is_enabled("christmas_lights_mode"):
        LightAction().add_light("Christmas Tree LEDs").turn_off()

def on_sleep_state_disabled(event):
    logger.info("Sleep state disabled")
    
    SwitchAction().add_switch("master_bedroom_whitenoise").turn_off()
    LightAction().add_lights(["First Floor Staircase LED"]).turn_off()
    ThermostatAction().add_thermostat("Master Bedroom Minisplit").turn_off()

    if state_machine.is_jim_home():
        JoinAction().add_target("jim_cell").send_taker_command("awake_command")

    if state_machine.is_heating_enabled():
        heat_action = ThermostatAction().add_thermostat("Oil Thermostat")
        heat_action.set_temperature(state_machine.get_number("normal_heat"), 'heat')

    if state_machine.is_enabled("christmas_lights_mode"):
        LightAction().add_light("Christmas Tree LEDs").turn_on_no_brightness()
        SwitchAction().add_switches([
            "Smart Strip Outlet 1",
            "Smart Strip Outlet 2",
            "Smart Strip Outlet 3",
            "Smart Strip Outlet 4"
        ]).turn_off()
    