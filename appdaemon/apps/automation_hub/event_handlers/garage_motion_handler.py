import event_dispatcher
import timer_manager
from util import logger
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from actions.light_action import LightAction
import state_machine

def motion_event_filter(event):
    return event.name in ["garage_back_motion", "garage_front_motion"]

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=motion_event_filter)
    event_dispatcher.register_callback(on_motion_cleared, MotionClearedEvent.__name__, event_filter=motion_event_filter)
    
def on_motion_triggered(event):
    logger.info("Garage motion detected")
    
    timer_manager.cancel_timer("garage_motion_timer")
    if state_machine.is_enabled("motion_lighting"):
        LightAction().add_light("garage_lights").turn_on()

def on_motion_cleared(event):
    logger.info("Garage motion cleared")
    timer_manager.start_timer("garage_motion_timer", lights_off, minutes=20)
    
def lights_off():
    if state_machine.is_enabled("motion_lighting"):
        LightAction().add_light("garage_lights").turn_off()
    