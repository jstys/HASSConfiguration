import functools

from automation_hub import event_dispatcher
from automation_hub import state_machine
from automation_hub import timer_manager
from util import logger
from events.power_sensor_off_event import PowerSensorOffEvent
from events.power_sensor_on_event import PowerSensorOnEvent
from actions.tts_action import TTSAction

def washer_filter(event):
    return event.name == "washer_running"
    
def dryer_filter(event):
    return event.name == "dryer_running"

def register_callbacks():
    event_dispatcher.register_callback(on_washer_on_event, PowerSensorOnEvent.__name__, event_filter=washer_filter)
    event_dispatcher.register_callback(on_washer_off_event, PowerSensorOffEvent.__name__, event_filter=washer_filter)
    event_dispatcher.register_callback(on_dryer_on_event, PowerSensorOnEvent.__name__, event_filter=dryer_filter)
    event_dispatcher.register_callback(on_dryer_off_event, PowerSensorOffEvent.__name__, event_filter=dryer_filter)
    
def on_washer_on_event(event):
    logger.info("Washer turned on")

def on_washer_off_event(event):
    logger.info("Washer turned off")
    if not state_machine.get_state(state_machine.SLEEP_STATE):
        TTSAction().broadcast("Washing machine has finished")

def on_dryer_on_event(event):
    logger.info("Dryer turned on")

def on_dryer_off_event(event):
    logger.info("Dryer turned off")
    if not state_machine.get_state(state_machine.SLEEP_STATE):
        TTSAction().broadcast("Dryer has finished")