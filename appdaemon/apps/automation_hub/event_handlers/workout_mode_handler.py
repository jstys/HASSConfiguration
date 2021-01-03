import event_dispatcher
import timer_manager
from util import logutil
from util import hassutil
from events.input_event import InputEvent
from actions.light_action import LightAction
from actions.media_player_action import MediaPlayerAction

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name == "workout_mode"

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
    hassutil.activate_scene("workout_mode")

def on_disabled(event):
    MediaPlayerAction().add_media_player("basement_tv").turn_off()
    LightAction().add_light("basement_fan").turn_off()

    light_action = LightAction().add_light("basement_lights").turn_off
    timer_manager.start_timer("basement_stairs_motion_timer", light_action, minutes=10)