from automation_hub import event_dispatcher
from automation_hub import state_machine
from util import logger
from events.mqtt_event import MQTTEvent

def event_filter(event):
    return "hermes/intent/" in event.topic

def register_callbacks():
    event_dispatcher.register_callback(on_intent, MQTTEvent.__name__, event_filter=event_filter)
    
def on_intent(event):
    source = event.payload.get("siteId")
    raw = event.payload.get("input")
    intent = event.payload.get("intent")
    if intent and source and raw:
        logger.info("Received Snips intent from {} with raw input ({})".format(source, raw))
        name = intent.get("intentName")
        if name == "jstys:thermostatSet":
            handle_thermostat(intent, source, raw)
        elif name == "jstys:tvOn":
            handle_tv_on(intent, source, raw)
        elif name == "jstys:tvOff":
            handle_tv_off(intent, source, raw)
        elif name == "jstys:lightOn":
            handle_light_on(intent, source, raw)
        elif name == "jstys:lightOff":
            handle_light_off(intent, source, raw)
    else:
        logger.error("Missing valid snips intent")

def handle_thermostat(intent, source, raw):
    logger.info("Received Thermostat set intent from snips")

def handle_tv_on(intent, source, raw):
    logger.info("Received TV On intent from snips")

def handle_tv_off(intent, source, raw):
    logger.info("Received TV Off intent from snips")

def handle_light_on(intent, source, raw):
    logger.info("Received Light On intent from snips")

def handle_light_off(intent, source, raw):
    logger.info("Received Light off intent from snips")
    