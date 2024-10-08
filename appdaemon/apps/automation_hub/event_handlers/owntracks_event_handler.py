import json

import event_dispatcher
from util import hassutil
from events.mqtt_event import MQTTEvent

status_map = {}

def event_filter(event: MQTTEvent):
    return event.topic.startswith("owntracks/")

def register_callbacks():
    event_dispatcher.register_callback(on_owntracks_event, MQTTEvent.__name__, event_filter=event_filter)

def on_owntracks_event(event: MQTTEvent):
    owntracks_user = event.topic.split("/")
    if len(owntracks_user) == 3:
        owntracks_user = owntracks_user[2]
        owntracks_json = json.loads(event.payload)
        payload_type = owntracks_json['_type']
        if payload_type == "lwt":
            hassutil.set_state(hassutil.Entity(f"binary_sensor.{owntracks_user}_owntracks_connected"), "off")
            status_map[owntracks_user] = False
        elif payload_type == "encrypted":
            hassutil.set_state(hassutil.Entity(f"binary_sensor.{owntracks_user}_owntracks_connected"), "on")
            status_map[owntracks_user] = True