import event_dispatcher
from util import logutil
from util import hassutil
from util.entity_map import name_map
from events.button_click_event import ButtonClickEvent
import state_machine

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

    hassutil.toggle(hassutil.Entity(name_map["workout_mode"]))
