import functools

from automation_hub import event_dispatcher
from automation_hub import timer_manager
from util import logutil
from events.motion_triggered_event import MotionTriggeredEvent
from actions.light_action import LightAction

logger = logutil.get_logger("automation_hub")

def motion_event_filter(event):
    return event.name in ["garage_back_motion", "garage_front_motion"]

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=motion_event_filter)
    
def on_motion_triggered(event):
    logger.info("Garage motion detected")
    
    timer_manager.cancel_timer("garage_motion_timer")
    timer_manager.start_timer("garage_motion_timer", lights_off, minutes=20)
    
    LightAction().add_light("front_garage_light").turn_on()
    
def lights_off():
    LightAction().add_light("front_garage_light").turn_off()
    