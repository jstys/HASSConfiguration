import event_dispatcher
from util import logger
from events.door_closed_event import DoorClosedEvent
from events.door_open_event import DoorOpenEvent
from actions.light_action import LightAction
from actions.push_notify_action import PushNotifyAction

def event_filter(event):
    return event.name == "Garage Door Sensor Contact"

def register_callbacks():
    event_dispatcher.register_callback(on_door_closed, DoorClosedEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_door_opened, DoorOpenEvent.__name__, event_filter=event_filter)
    
def on_door_closed(event):
    logger.info("Garage door closed")
    PushNotifyAction().add_target("jim_cell").set_message("Garage door closed", notification_id="garage-door-state").notify()

def on_door_opened(event):
    logger.info("Garage door opened")
    PushNotifyAction().add_target("jim_cell").set_message("Garage door opened", notification_id="garage-door-state").notify()
    LightAction().add_light("Garage Lights").turn_on()
    