import event_dispatcher
import state_machine
import timer_manager
from util import logger
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name == "Hallway Motion Sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_motion_cleared, MotionClearedEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Hallway motion detected")

    timer_manager.cancel_timer("hallway_motion_timer")
    if not state_machine.is_enabled("indoor_movie_mode", "privacy_mode") and state_machine.is_enabled("motion_lighting"):
        if not state_machine.is_enabled("sleep_mode"):
            LightAction().add_light("Hallway Lights").turn_on()
        else:
            LightAction().add_lights(["First Floor Staircase LED"]).turn_on()

def on_motion_cleared(event):
    logger.info("Hallway motion cleared")
    timer_manager.start_timer("hallway_motion_timer", lights_off, minutes=5)

def lights_off():
    if state_machine.is_enabled("motion_lighting"):
        if not state_machine.is_enabled("sleep_mode"):
            LightAction().add_lights(["Hallway Lights"]).turn_off()
        else:
            LightAction().add_lights(["First Floor Staircase LED"]).turn_off()