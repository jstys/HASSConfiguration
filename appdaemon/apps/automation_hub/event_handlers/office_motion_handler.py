import event_dispatcher
import state_machine
from util import logger
from events.motion_triggered_event import MotionTriggeredEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name == "office_motion_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Office motion detected")
    
    if not state_machine.is_enabled("sleep_mode") and state_machine.is_enabled("motion_lighting"):
        LightAction().add_light("office_lights").turn_on()