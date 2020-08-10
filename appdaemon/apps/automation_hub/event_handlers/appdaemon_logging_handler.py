from automation_hub import event_dispatcher
from util import logutil
from events.input_event import InputEvent

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name == "appdaemon_log_mode"

def register_callbacks():
    event_dispatcher.register_callback(on_change_event, InputEvent.__name__, event_filter=event_filter)  

def on_change_event(event):
    if event.new == "normal":
        logger.set_level("normal")
    elif event.old == "debug":
        logger.set_level("debug")

