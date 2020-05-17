import functools

from automation_hub import event_dispatcher
from automation_hub import timer_manager
from automation_hub import state_machine
from util import logutil
from events.motion_triggered_event import MotionTriggeredEvent
from actions.light_action import LightAction

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name in ["grill_area_motion"]

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Grill area motion detected")
    
    timer_manager.cancel_timer("grill_area_motion_timer")
    timer_manager.start_timer("grill_area_motion_timer", lights_off, minutes=30)
    
    if not state_machine.is_sun_up():
        LightAction().add_light("grill_light_fixture").turn_on()
    
def lights_off():
    LightAction().add_light("grill_light_fixture").turn_off()
