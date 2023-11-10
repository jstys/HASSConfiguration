import event_dispatcher
import timer_manager
import state_machine
from util import logger
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name in ["Fourth Bedroom Motion Sensor"]

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_motion_cleared, MotionClearedEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Fourth bedroom motion detected")
    
    timer_manager.cancel_timer("fourth_bedroom_motion_timer")
    if state_machine.is_enabled("Motion Lighting"):
        LightAction().add_light("Fourth Bedroom Fixture").turn_on()
    
def on_motion_cleared(event):
    logger.info("Fourth bedroom motion cleared")
    timer_manager.start_timer("fourth_bedroom_motion_timer", lights_off, minutes=15)

def lights_off():
    if state_machine.is_enabled("Motion Lighting"):
        LightAction().add_light("Fourth Bedroom Fixture").turn_off()
