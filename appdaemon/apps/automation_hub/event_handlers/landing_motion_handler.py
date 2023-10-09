import event_dispatcher
import timer_manager
import state_machine
from util import logger
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name == "Landing Motion Sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_motion_cleared, MotionClearedEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Landing motion detected")

    timer_manager.cancel_timer("landing_motion_timer")
    
    if not state_machine.is_enabled("indoor_movie_mode") and state_machine.is_enabled("motion_lighting"):    
        LightAction().add_light("Landing Light").turn_on()

def on_motion_cleared(event):
    logger.info("Landing motion cleared")

    timer_manager.start_timer("landing_motion_timer", lights_off, minutes=5)

def lights_off():
    if state_machine.is_enabled("motion_lighting"):
        LightAction().add_light("Landing Light").turn_off()