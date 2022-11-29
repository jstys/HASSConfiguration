import json

import event_dispatcher
from util import logger
from events.mqtt_event import MQTTEvent
from actions.push_notify_action import PushNotifyAction

status_map = {}

def event_filter(event: MQTTEvent):
    return event.topic.startswith("owntracks/owntracks")

def register_callbacks():
    event_dispatcher.register_callback(on_owntracks_event, MQTTEvent.__name__, event_filter=event_filter)

def on_owntracks_event(event: MQTTEvent):
    owntracks_user = event.topic.split("/")[-1]
    owntracks_json = json.loads(event.payload)
    payload_type = owntracks_json['_type']
    if payload_type == "lwt":
        PushNotifyAction().add_targets("jim_cell").set_message(f"{owntracks_user} is offline", notification_id=f"owntracks-{owntracks_user}-status").notify()
        status_map[owntracks_user] = False
    elif payload_type == "encrypted":
        if owntracks_user in status_map and not status_map[owntracks_user]:
            PushNotifyAction().add_targets("jim_cell").set_message(f"{owntracks_user} is online again", notification_id=f"owntracks-{owntracks_user}-status").notify()
            status_map[owntracks_user] = True