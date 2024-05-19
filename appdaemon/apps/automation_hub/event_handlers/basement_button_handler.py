import event_dispatcher
from util import logger
from util import hassutil
from util.entity_map import name_map
from events.mqtt_event import MQTTEvent
from actions.switch_action import SwitchAction

def event_filter(event: MQTTEvent):
    parts = event.topic.split("/")
    return len(parts) == 3 and parts[0] == "zigbee2mqtt" and parts[1] == "basement_button" and parts[2] == "action"


def register_callbacks():
    event_dispatcher.register_callback(on_button_clicked, MQTTEvent.__name__, event_filter=event_filter)
    
def on_button_clicked(event: MQTTEvent):
    if event.payload == "single":
        on_single_click(event)
    elif event.payload == "long":
        on_long_press(event)

def on_long_press(event):
    logger.info("Basement Button single clicked")

    hassutil.toggle(hassutil.Entity(name_map["Workout Mode"]))

def on_single_click(event):
    logger.info("Basement Button long press")

    SwitchAction().add_switch("Basement Fans").toggle()
