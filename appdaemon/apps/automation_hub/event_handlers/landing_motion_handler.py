import functools

from automation_hub import event_dispatcher
from automation_hub import state_machine
from automation_hub import timer_manager
from util import logger
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name == "landing_motion_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_motion_cleared, MotionClearedEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Landing motion detected")
    
    timer_manager.cancel_timer("landing_motion_timer")
    timer_manager.start_timer("landing_motion_timer", functools.partial(on_motion_cleared, "landing_motion_timer"), minutes=20)
    
    LightAction().add_light("landing_light").turn_on()

def on_motion_cleared(event):
    logger.info("Landing motion cleared")
    
    if event != "landing_motion_timer":
        timer_manager.cancel_timer("landing_motion_timer")
    LightAction().add_light("landing_light").turn_off()