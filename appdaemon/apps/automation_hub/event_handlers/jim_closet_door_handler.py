import event_dispatcher
import timer_manager
from util import logger
from events.door_open_event import DoorOpenEvent
from events.door_closed_event import DoorClosedEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name == "jim_closet_door_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_door_opened, DoorOpenEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_door_closed, DoorClosedEvent.__name__, event_filter=event_filter)
    
def on_door_opened(event):
    logger.info("Jim Closet door opened")

    timer_manager.cancel_timer("jim_closet_door_timer")
    
    LightAction().add_light("jim_closet_light").turn_on()

def on_door_closed(event):
    logger.info("Jim Closet door closed")
    timer_manager.start_timer("jim_closet_door_timer", lights_off, minutes=5)

def lights_off():
    LightAction().add_lights(["jim_closet_light"]).turn_off()