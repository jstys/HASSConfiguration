from automation_hub import event_dispatcher
from util import logger
from events.door_closed_event import DoorClosedEvent
from events.door_open_event import DoorOpenEvent

def event_filter(event):
    return event.name == "front_door_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_door_closed, DoorClosedEvent().__class__.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_door_opened, DoorOpenEvent().__class__.__name__, event_filter=event_filter)
    
def on_door_closed(event):
    logger.info("Front door closed")

def on_door_opened(event):
    logger.info("Front door opened")