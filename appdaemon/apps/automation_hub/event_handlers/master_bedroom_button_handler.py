import event_dispatcher
from util import logger
from util import hassutil
from util.entity_map import name_map
from events.mqtt_event import MQTTEvent
from actions.media_player_action import MediaPlayerAction
from actions.light_action import LightAction
import state_machine

def event_filter(event: MQTTEvent):
    return event.topic.startswith("zigbee2mqtt") and event.topic.endswith("action")

def register_callbacks():
    event_dispatcher.register_callback(on_button_clicked, MQTTEvent.__name__, event_filter=event_filter)
    
def on_button_clicked(event: MQTTEvent):
    device = event.topic.split("/")[1]
    if device == "master_bedroom_button":
        if event.payload == "single":
            on_single_click(event)
        elif event.payload == "double":
            on_double_click(event)
        elif event.payload == "long":
            on_long_press(event)
    elif device == "master_bedroom_closet_button":
        if event.payload == "single":
            on_closet_single_click(event)

def on_closet_single_click(event):
    logger.info("Master Bedroom Closet Button single clicked")

    LightAction().add_light("Master Bedroom Closet Lights").toggle()

def on_single_click(event):
    logger.info("Master Bedroom Button single clicked")

    if state_machine.is_enabled("Sleep Mode"):
        hassutil.toggle(hassutil.Entity(name_map["Master Bedroom Whitenoise"]))
    else:
        hassutil.toggle(hassutil.Entity(name_map["Privacy Mode"]))

def on_double_click(event):
    logger.info("Master Bedroom Button double clicked")

    MediaPlayerAction().add_media_player("Master Bedroom TV").toggle_power()

def on_long_press(event):
    logger.info("Master Bedroom Button long pressed")

    hassutil.toggle(hassutil.Entity(name_map["Sleep Mode"]))
