import functools

from automation_hub import event_dispatcher
from automation_hub import state_machine
from automation_hub import timer_manager
from util import logutil
from events.xiaomi_motion_triggered_event import XiaomiMotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from actions.light_action import LightAction

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name == "office_motion_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, XiaomiMotionTriggeredEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_motion_cleared, MotionClearedEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Office motion detected")
    
    LightAction().add_light("office_lights").turn_on()

def on_motion_cleared(event):
    logger.info("Office motion cleared")