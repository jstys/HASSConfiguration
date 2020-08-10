import functools

from automation_hub import event_dispatcher
from automation_hub import state_machine
from automation_hub import timer_manager
from util import logutil
from events.motion_triggered_event import MotionTriggeredEvent
from actions.light_action import LightAction

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name == "office_motion_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Office motion detected")
    
    if not state_machine.is_sleep_state_enabled():
        LightAction().add_light("office_lights").turn_on()