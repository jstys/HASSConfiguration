import event_dispatcher
import timer_manager
import state_machine
from util import logger
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name in ["Basement Stairs Motion Sensor"]

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_motion_cleared, MotionClearedEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Basement stairs motion detected")

    timer_manager.cancel_timer("basement_stairs_motion_timer")
    timer_manager.cancel_timer("landing_motion_timer")
    if not state_machine.is_enabled("Indoor Movie Mode") and state_machine.is_enabled("Motion Lighting"):
        LightAction().add_light("Landing Light").turn_on()
    
    if not state_machine.is_enabled("Sleep Mode") and state_machine.is_enabled("Motion Lighting"):
        LightAction().add_light("Basement Lights").turn_on()

def on_motion_cleared(event):
    logger.info("Basement stairs motion cleared")
    
    timer_manager.start_timer("landing_motion_timer", landing_light_off, minutes=5)
    if not state_machine.is_enabled("Workout Mode"):
        timer_manager.start_timer("basement_stairs_motion_timer", basement_lights_off, minutes=10)
    
def landing_light_off():
    if state_machine.is_enabled("Motion Lighting"):
        LightAction().add_light("Landing Light").turn_off()

def basement_lights_off():
    if state_machine.is_enabled("Motion Lighting"):
        LightAction().add_light("Basement Lights").turn_off()
