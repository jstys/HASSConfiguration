import functools

from automation_hub import event_dispatcher
from automation_hub import state_machine
from automation_hub import timer_manager
from util import logger
from events.xiaomi_motion_triggered_event import XiaomiMotionTriggeredEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name == "garage_motion_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, XiaomiMotionTriggeredEvent.__name__, event_filter=event_filter)
    
def on_motion_triggered(event):
    logger.info("Garage motion detected")
    
    timer_manager.cancel_timer("garage_motion_timer")
    timer_manager.start_timer("garage_motion_timer", lights_off, minutes=20)
    
    LightAction().add_light("front_garage_light").turn_on()
    
def lights_off():
    LightAction().add_light("front_garage_light").turn_off()
    