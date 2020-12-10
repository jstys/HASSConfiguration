import functools

from automation_hub import event_dispatcher
from automation_hub import timer_manager
from automation_hub import state_machine
from util import logutil
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from actions.light_action import LightAction

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name in ["basement_stairs_motion"]

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_motion_cleared, MotionClearedEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Basement stairs motion detected")

    timer_manager.cancel_timer("basement_stairs_motion_timer")
    if not state_machine.is_enabled("indoor_movie_mode") and state_machine.is_enabled("motion_lighting"):
        LightAction().add_light("landing_light").turn_on()
    
    if not state_machine.is_enabled("sleep_mode") and state_machine.is_enabled("motion_lighting"):
        LightAction().add_light("basement_lights").turn_on()

def on_motion_cleared(event):
    logger.info("Basement stairs motion cleared")
    
    if state_machine.is_enabled("motion_lighting"):
        timer_manager.start_timer("landing_motion_timer", landing_light_off, minutes=5)
        if not state_machine.is_enabled("workout_mode"):
            timer_manager.start_timer("basement_stairs_motion_timer", basement_lights_off, minutes=10)
    
def landing_light_off():
    LightAction().add_light("landing_light").turn_off()

def basement_lights_off():
    LightAction().add_light("basement_lights").turn_off()
