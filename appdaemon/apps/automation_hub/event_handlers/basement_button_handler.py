from automation_hub import event_dispatcher
from util import logutil
from events.button_click_event import ButtonClickEvent
from actions.media_player_action import MediaPlayerAction
from actions.light_action import LightAction
from automation_hub import state_machine

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.button_name == "basement_button"


def register_callbacks():
    event_dispatcher.register_callback(on_button_clicked, ButtonClickEvent.__name__, event_filter=event_filter)
    
def on_button_clicked(event):
    if event.click_type == "single":
        on_single_click(event)

def on_single_click(event):
    logger.info("Basement Button single clicked")

    MediaPlayerAction().add_media_player("basement_tv").toggle_power()
    LightAction().add_light("basement_fan").toggle()
