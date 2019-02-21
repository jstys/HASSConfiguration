import functools

from automation_hub import event_dispatcher
from automation_hub import state_machine
from automation_hub import timer_manager
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
    
    timer_manager.cancel_timer("hallway_motion_timer")
    timer_manager.start_timer("hallway_motion_timer", functools.partial(on_motion_cleared, "hallway_motion_timer"), minutes=20)
    
    if not state_machine.get_state(state_machine.SLEEP_STATE):
        LightAction().add_light("hallway_lights").turn_on()
    else:
        LightAction().add_lights(["gateway_light", "first_floor_staircase_led"]).turn_on()

def on_motion_cleared(event):
    logger.info("Hallway motion cleared")
    
    if event != "hallway_motion_timer":
        timer_manager.cancel_timer("hallway_motion_timer")
    LightAction().add_lights(["hallway_lights", "gateway_light", "first_floor_staircase_led"]).turn_off()