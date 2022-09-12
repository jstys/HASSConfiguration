import event_dispatcher
import timer_manager
from util import logger
from events.door_open_event import DoorOpenEvent
from events.door_closed_event import DoorClosedEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name == "attic_door_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_door_opened, DoorOpenEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_door_closed, DoorClosedEvent.__name__, event_filter=event_filter)
    
def on_door_opened(event):
    logger.info("Attic door opened")

    timer_manager.cancel_timer("attic_door_timer")
    
    LightAction().add_light("attic_lights").turn_on()

def on_door_closed(event):
    logger.info("Attic door closed")
    timer_manager.start_timer("attic_door_timer", lights_off, minutes=20)

def lights_off():
    LightAction().add_lights(["attic_lights"]).turn_off()