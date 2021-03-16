import event_dispatcher
import state_machine
from util import logutil
from events.door_closed_event import DoorClosedEvent
from events.door_open_event import DoorOpenEvent
from events.lock_event import LockEvent
from events.door_lock_notification_locked_event import DoorLockNotificationLockedEvent
from events.door_lock_notification_unlocked_event import DoorLockNotificationUnlockedEvent
from actions.push_notify_action import PushNotifyAction

logger = logutil.get_logger("automation_hub")

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
    event_dispatcher.register_callback(on_door_locked_notification, DoorLockNotificationLockedEvent.__name__, event_filter=notify_filter)
    event_dispatcher.register_callback(on_door_unlocked_notification, DoorLockNotificationUnlockedEvent.__name__, event_filter=notify_filter)
    
def on_door_locked_notification(event):
    state_machine.set_state("front_entrance_lock", "locked")

def on_door_unlocked_notification(event):
    state_machine.set_state("front_entrance_lock", "unlocked")

def on_door_closed(event):
    logger.info("Front door closed")

def on_door_opened(event):
    logger.info("Front door opened")

def on_door_lock_changed(event):
    if event.is_locked:
        logger.info("Front door locked")
        PushNotifyAction().add_target("jim_cell").set_message("Front door locked ({})".format(event.status)).notify()
    else:
        logger.info("Front door unlocked")
        PushNotifyAction().add_target("jim_cell").set_message("Front door Unlocked ({})".format(event.status)).notify()
