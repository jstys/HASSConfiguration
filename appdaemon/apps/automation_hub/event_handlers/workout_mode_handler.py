import event_dispatcher
import timer_manager
import state_machine
from util import logger
from util import hassutil
from events.input_event import InputEvent
from actions.light_action import LightAction
from actions.switch_action import SwitchAction
from actions.media_player_action import MediaPlayerAction
from actions.thermostat_action import ThermostatAction

def event_filter(event):
    return event.name == "Workout Mode"

def register_callbacks():
    event_dispatcher.register_callback(on_state_changed, InputEvent.__name__, event_filter=event_filter)
    
def on_state_changed(event):
    if event.new == "off":
        on_disabled(event)
    elif event.new == "on":
        on_enabled(event)
    else:
        logger.warning("Invalid state transition for workout mode")

def on_enabled(event):
    hassutil.activate_scene("Workout Mode")

    if state_machine.is_heating_enabled():
        ThermostatAction().add_thermostat("Oil Thermostat").turn_off()

def on_disabled(event):
    MediaPlayerAction().add_media_player("Basement TV").turn_off()
    SwitchAction().add_switches(["Basement Fan Switch", "Basement Treadmill Fan"]).turn_off()

    light_action = LightAction().add_light("Basement Lights").turn_off
    timer_manager.start_timer("basement_stairs_motion_timer", light_action, minutes=10)

    if state_machine.is_heating_enabled():
        heat_action = ThermostatAction().add_thermostat("Oil Thermostat")
        heat_action.turn_on()
        heat_action.set_temperature(state_machine.get_number("Normal Heat"), "heat")