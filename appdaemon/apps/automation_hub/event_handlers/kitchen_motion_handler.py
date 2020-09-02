import functools

from automation_hub import event_dispatcher
from automation_hub import timer_manager
from automation_hub import state_machine
from util import logutil
from events.motion_triggered_event import MotionTriggeredEvent
from actions.light_action import LightAction

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name in ["kitchen_front_motion"]

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Kitchen motion detected")
    
    if not state_machine.is_enabled("outdoor_movie_mode", "indoor_movie_mode"):
        timer_manager.cancel_timer("kitchen_motion_timer")
        timer_manager.start_timer("kitchen_motion_timer", lights_off, minutes=30)

        LightAction().add_light("kitchen_cabinet_lights").turn_on(color_temp=400)

        if not state_machine.is_enabled("sleep_mode"):
            LightAction().add_light("kitchen_lights").turn_on()
    
def lights_off():
    LightAction().add_lights(["kitchen_lights", "kitchen_cabinet_lights"]).turn_off()
