from automation_hub import event_dispatcher
from automation_hub import state_machine
from util import logger
from events.zwave_scene_event import ZwaveSceneEvent
from actions.light_action import LightAction

def event_filter(event):
    return event.name in ["fibaro_keychain"]

def register_callbacks():
    event_dispatcher.register_callback(on_scene_activated, ZwaveSceneEvent.__name__, event_filter=event_filter)
    
def on_scene_activated(event):
    if event.scene_id == 1:
        on_square_pressed(event)
    elif event.scene_id == 2:
        on_circle_pressed(event)
    elif event.scene_id == 3:
        on_x_pressed(event)
    elif event.scene_id == 4:
        on_triangle_pressed(event)
    elif event.scene_id == 5:
        on_minus_pressed(event)
    elif event.scene_id == 6:
        on_plus_pressed(event)
    
def on_square_pressed(event):
    logger.info("Square button pressed")

def on_circle_pressed(event):
    logger.info("Circle button pressed")

def on_x_pressed(event):
    logger.info("X button pressed")

def on_triangle_pressed(event):
    logger.info("Triangle button pressed")

def on_minus_pressed(event):
    logger.info("Minus button pressed")

def on_plus_pressed(event):
    logger.info("Plus button pressed")
    