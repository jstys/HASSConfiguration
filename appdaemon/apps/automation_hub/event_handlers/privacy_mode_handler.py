import event_dispatcher
from util import logger
from util import hassutil
from events.input_event import InputEvent

def event_filter(event):
    return event.name == "privacy_mode"

def register_callbacks():
    event_dispatcher.register_callback(on_state_changed, InputEvent.__name__, event_filter=event_filter)
    
def on_state_changed(event):
    if event.new == "off":
        pass
    elif event.new == "on":
        on_enabled(event)
    else:
        logger.warning("Invalid state transition for privacy mode")

def on_enabled(event):
    hassutil.activate_scene("privacy_mode")
