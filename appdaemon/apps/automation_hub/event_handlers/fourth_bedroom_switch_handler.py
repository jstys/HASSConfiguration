from automation_hub import event_dispatcher
from automation_hub import state_machine
from util import logger
from events.mqtt_event import MQTTEvent
from actions.light_action import LightAction

def event_filter(event):
    return "smartthings/fourth_bedroom_switch/button" in event.topic

def register_callbacks():
    event_dispatcher.register_callback(on_message, MQTTEvent.__name__, event_filter=event_filter)
    
def on_message(event):
    topic = event.topic
    payload = event.payload
    
    logger.info("Received Fourth Bedroom MQTT message with topic: {} and payload: {}".format(topic, payload))

    if payload == "pushed":
        handle_pushed()

def handle_pushed():
    LightAction().add_light("fourth_bedroom_fixture").toggle()
    