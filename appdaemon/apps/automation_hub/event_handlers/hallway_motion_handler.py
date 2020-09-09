import functools

from automation_hub import event_dispatcher
from automation_hub import state_machine
from automation_hub import timer_manager
from util import logutil
from events.motion_triggered_event import MotionTriggeredEvent
from actions.light_action import LightAction

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name == "hallway_motion_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Hallway motion detected")

    if not state_machine.is_enabled("indoor_movie_mode", "privacy_mode"):
        timer_manager.cancel_timer("hallway_motion_timer")
        
        if not state_machine.is_enabled("sleep_mode"):
            LightAction().add_light("hallway_lights").turn_on()
        else:
            LightAction().add_lights(["first_floor_staircase_led"]).turn_on()

        timer_manager.start_timer("hallway_motion_timer", lights_off, minutes=5)

def lights_off():
    if not state_machine.is_enabled("sleep_mode"):
        LightAction().add_lights(["hallway_lights"]).turn_off()
    else:
        LightAction().add_lights(["first_floor_staircase_led"]).turn_off()