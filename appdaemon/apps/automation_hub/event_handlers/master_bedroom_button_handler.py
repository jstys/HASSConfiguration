import event_dispatcher
from util import logutil
from util import hassutil
from util.entity_map import name_map
from events.button_click_event import ButtonClickEvent
from actions.media_player_action import MediaPlayerAction
from actions.switch_action import SwitchAction
from actions.light_action import LightAction
import state_machine

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.button_name == "master_bedroom_button"

def closet_filter(event):
    return event.button_name == "master_bedroom_closet_button"

def register_callbacks():
    event_dispatcher.register_callback(on_button_clicked, ButtonClickEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_closet_button_clicked, ButtonClickEvent.__name__, event_filter=closet_filter)
    
def on_button_clicked(event):
    if event.click_type == "single":
        on_single_click(event)
    elif event.click_type == "double":
        on_double_click(event)
    elif event.click_type == "long_click_press":
        on_long_press(event)

def on_closet_button_clicked(event):
    if event.click_type == "single":
        on_closet_single_click(event)

def on_closet_single_click(event):
    logger.info("Master Bedroom Closet Button single clicked")

    LightAction().add_light("master_bedroom_closet_lights").toggle()

def on_single_click(event):
    logger.info("Master Bedroom Button single clicked")

    if state_machine.is_enabled("sleep_mode"):
        SwitchAction().add_switch("master_bedroom_whitenoise").toggle()
    else:
        SwitchAction().add_switch("privacy_mode").toggle()

def on_double_click(event):
    logger.info("Master Bedroom Button double clicked")

    MediaPlayerAction().add_media_player("master_bedroom_tv").toggle_power()

def on_long_press(event):
    logger.info("Master Bedroom Button long pressed")

    hassutil.toggle(hassutil.Entity(name_map["sleep_mode"]))
