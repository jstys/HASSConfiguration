from automation_hub import event_dispatcher
from automation_hub import state_machine
from automation_hub import timer_manager
from util import logger
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name == "office_motion_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Office motion detected")
    
    timer_manager.cancel_timer("office_motion_timer")
    timer_manager.start_timer("office_motion_timer", on_motion_cleared, minutes=1)
    
    LightAction().add_light("office_lights").turn_on()

def on_motion_cleared():
    logger.info("Office motion cleared")