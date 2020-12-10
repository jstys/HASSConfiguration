from automation_hub import event_dispatcher
from util import logutil
from util import hassutil
from events.input_event import InputEvent
from actions.light_action import LightAction
from actions.join_action import JoinAction
from actions.thermostat_action import ThermostatAction

logger = logutil.get_logger("automation_hub")

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
    JoinAction().add_target("jim_cell").send_taker_command("bed_command")

def on_sleep_state_disabled(event):
    logger.info("Sleep state disabled")
    
    JoinAction().add_target("jim_cell").send_taker_command("awake_command")
    LightAction().add_lights(["first_floor_staircase_led"]).turn_off()
    ThermostatAction().add_thermostat("master_bedroom_ac").turn_off()
    