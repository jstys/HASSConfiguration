import event_dispatcher
from util import logger
from events.input_event import InputEvent

def event_filter(event):
    return event.name == "Appdaemon Log Mode"

def register_callbacks():
    event_dispatcher.register_callback(on_change_event, InputEvent.__name__, event_filter=event_filter)  

def on_change_event(event):
    if event.new == "normal":
        logger.set_level("normal")
    elif event.new == "debug":
        logger.set_level("debug")

