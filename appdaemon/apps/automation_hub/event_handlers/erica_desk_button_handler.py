import event_dispatcher
from util import logger
from events.mqtt_event import MQTTEvent
from actions.thermostat_action import ThermostatAction

def event_filter(event: MQTTEvent):
    parts = event.topic.split("/")
    return len(parts) == 3 and parts[0] == "zigbee2mqtt" and parts[1] == "erica_desk_button" and parts[2] == "action"


def register_callbacks():
    event_dispatcher.register_callback(on_button_clicked, MQTTEvent.__name__, event_filter=event_filter)
    
def on_button_clicked(event: MQTTEvent):
    if event.payload == "single":
        on_single_click(event)

def on_single_click(event):
    logger.info("Erica Desk Button click")

    ThermostatAction().add_thermostat("Office Minisplit").toggle()
