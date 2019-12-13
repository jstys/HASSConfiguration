import functools

from automation_hub import event_dispatcher
from automation_hub import timer_manager
from util import logger
from events.power_sensor_off_event import PowerSensorOffEvent
from events.power_sensor_on_event import PowerSensorOnEvent
from actions.push_notify_action import PushNotifyAction

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
    timer_manager.cancel_timer("laundry_washer_timer")

def on_washer_off_event(event):
    logger.info("Washer turned off")
    timer_manager.start_timer("laundry_washer_timer", on_washer_finished, minutes=6)

def on_washer_finished():
    PushNotifyAction().add_targets(["jim_cell", "erica_cell"]).set_message("Washing Machine has finished").notify()

def on_dryer_on_event(event):
    logger.info("Dryer turned on")

def on_dryer_off_event(event):
    logger.info("Dryer turned off")
    PushNotifyAction().add_targets(["jim_cell", "erica_cell"]).set_message("Dryer has finished").notify()