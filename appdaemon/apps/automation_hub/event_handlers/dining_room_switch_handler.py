import event_dispatcher
from util import logger
from events.zwave_scene_event import ZwaveSceneEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name in ["dining_room_switch"]

def register_callbacks():
    event_dispatcher.register_callback(on_scene_activated, ZwaveSceneEvent.__name__, event_filter=event_filter)
    
def on_scene_activated(event):
    if event.scene_id == 1:
        on_top_button(event)
    elif event.scene_id == 2:
        on_bottom_button(event)

def on_top_button(event):
    logger.info("Turning on dining room light")
    LightAction().add_light("dining_room_light").turn_on(color_temp=255)

def on_bottom_button(event):
    logger.info("Turning off dining room light")
    LightAction().add_light("dining_room_light").turn_off()