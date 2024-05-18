import event_dispatcher
from util import logger
from events.mqtt_event import MQTTEvent
from actions.push_notify_action import PushNotifyAction
from actions.discord_notify_action import DiscordNotifyAction

def event_filter(event: MQTTEvent):
    return event.topic.startswith("amcrest2mqtt/")

def register_callbacks():
    event_dispatcher.register_callback(on_doorbell_event, MQTTEvent.__name__, event_filter=event_filter)

def on_doorbell_event(event: MQTTEvent):
    doorbell_event = event.topic.split("/")[-1]
    if doorbell_event == "motion":
        on_doorbell_motion(event.payload)
    elif doorbell_event == "doorbell":
        on_doorbell_pushed(event.payload)
    else:
        logger.warning(f"Received invalid doorbell event {doorbell_event}")

def on_doorbell_motion(payload):
    if payload == 'on':
        logger.info("Doorbell motion detected")
        PushNotifyAction().add_target("jim_cell").set_message("Motion at front door", notification_id="hass-doorbell-motion").notify()
    elif payload == 'off':
        logger.info("Doorbell motion cleared")
    else:
        logger.warning(f"Received invalid motion payload {payload}")

def on_doorbell_pushed(payload):
    if payload == 'on':
        logger.info("Doorbell push detected")
        DiscordNotifyAction().set_message("Doorbell is ringing").add_channel("general").notify()
