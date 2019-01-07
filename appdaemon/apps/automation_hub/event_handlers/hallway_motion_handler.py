from automation_hub import event_dispatcher
from automation_hub import state_machine
from util import logger
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name == "hallway_motion_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_motion_cleared, MotionClearedEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Hallway motion detected")
    
    if not state_machine.get_state(state_machine.SLEEP_STATE):
        LightAction().add_light("hallway_lights").turn_on()

def on_motion_cleared(event):
    logger.info("Hallway motion cleared")
    
    LightAction().add_light("hallway_lights").turn_off()