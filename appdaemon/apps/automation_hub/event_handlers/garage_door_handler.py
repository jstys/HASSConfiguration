import event_dispatcher
import state_machine
from util import logutil
from events.door_closed_event import DoorClosedEvent
from events.door_open_event import DoorOpenEvent
from actions.light_action import LightAction

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name == "garage_door_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_door_closed, DoorClosedEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_door_opened, DoorOpenEvent.__name__, event_filter=event_filter)
    
def on_door_closed(event):
    logger.info("Garage door closed")

def on_door_opened(event):
    logger.info("Garage door opened")
    