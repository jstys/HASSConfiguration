from automation_hub import event_dispatcher
from util import logger
from events.zwave_scene_event import ZwaveSceneEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name in ["staircase_top_switch", "staircase_bottom_switch"]

def register_callbacks():
    event_dispatcher.register_callback(on_scene_activated, ZwaveSceneEvent.__name__, event_filter=event_filter)
    
def on_scene_activated(event):
    if event.scene_id == 1:
        on_top_button(event)
    elif event.scene_id == 2:
        on_bottom_button(event)

def on_top_button(event):
    LightAction().add_light("hallway_lights").turn_on()

def on_bottom_button(event):
    LightAction().add_light("hallway_lights").turn_off()