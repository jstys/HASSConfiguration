import event_dispatcher
from util import logutil
from events.mqtt_event import MQTTEvent

logger = logutil.get_logger("automation_hub")

def event_filter(event: MQTTEvent):
    return event.topic.startswith("amcrest2mqtt/")

def register_callbacks():
    event_dispatcher.register_callback(on_doorbell_event, MQTTEvent.__name__, event_filter=event_filter)

def on_doorbell_event(event: MQTTEvent):
    doorbell_event = event.topic.split("/")[-1]
    if doorbell_event == "motion":
        on_doorbell_motion(event.payload)
    elif doorbell_event == "doorbell":
        on_doorbell_pushed()
    else:
        logger.warning(f"Received invalid doorbell event {doorbell_event}")

def on_doorbell_motion(payload):
    if payload == 'on':
        logger.info("Doorbell motion detected")
    elif payload == 'off':
        logger.info("Doorbell motion cleared")
    else:
        logger.warning(f"Received invalid motion payload {payload}")

def on_doorbell_pushed():
    logger.info("Doorbell push detected")