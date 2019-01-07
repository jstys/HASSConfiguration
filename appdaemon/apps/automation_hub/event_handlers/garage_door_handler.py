from automation_hub import event_dispatcher
from automation_hub import state_machine
from util import logger
from events.door_closed_event import DoorClosedEvent
from events.door_open_event import DoorOpenEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name == "garage_door_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_door_closed, DoorClosedEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_door_opened, DoorOpenEvent.__name__, event_filter=event_filter)
    
def on_door_closed(event):
    logger.info("Garage door closed")
    
    LightAction().add_light("driveway_light").turn_off()

def on_door_opened(event):
    logger.info("Garage door opened")
    
    if not state_machine.get_state(state_machine.SUN_UP_STATE):
        LightAction().add_light("driveway_light").turn_on()
    