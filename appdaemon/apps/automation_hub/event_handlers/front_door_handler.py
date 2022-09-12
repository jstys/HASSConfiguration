import event_dispatcher
from util import logger
from events.door_closed_event import DoorClosedEvent
from events.door_open_event import DoorOpenEvent
from events.lock_event import LockEvent
from actions.push_notify_action import PushNotifyAction

def sensor_filter(event):
    return event.name == "front_entrance_door_sensor"

def lock_filter(event):
    return event.name == "front_entrance_lock"

def notify_filter(event):
    return event.name == "front_door_lock_alarmtype"

def register_callbacks():
    event_dispatcher.register_callback(on_door_closed, DoorClosedEvent.__name__, event_filter=sensor_filter)
    event_dispatcher.register_callback(on_door_opened, DoorOpenEvent.__name__, event_filter=sensor_filter)
    event_dispatcher.register_callback(on_door_lock_changed, LockEvent.__name__, event_filter=lock_filter)

def on_door_closed(event):
    logger.info("Front door closed")

def on_door_opened(event):
    logger.info("Front door opened")

def on_door_lock_changed(event: LockEvent):
    if event.is_locked:
        logger.info("Front door locked")
        PushNotifyAction().add_target("jim_cell").set_message("Front door locked", notification_id="front-door-lock").notify()
    else:
        logger.info("Front door unlocked")
        PushNotifyAction().add_target("jim_cell").set_message("Front door Unlocked", notification_id="front-door-lock").notify()
