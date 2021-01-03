import event_dispatcher
from util import logutil
from util import hassutil
from events.input_event import InputEvent

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name == "indoor_movie_mode"

def register_callbacks():
    event_dispatcher.register_callback(on_state_changed, InputEvent.__name__, event_filter=event_filter)
    
def on_state_changed(event):
    if event.new == "off":
        pass
    elif event.new == "on":
        on_enabled(event)
    else:
        logger.warning("Invalid state transition for indoor movie mode")

def on_enabled(event):
    hassutil.activate_scene("indoor_movie_mode")
