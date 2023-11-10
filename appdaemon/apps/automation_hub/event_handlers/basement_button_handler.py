import event_dispatcher
from util import logger
from util import hassutil
from util.entity_map import name_map
from events.button_click_event import ButtonClickEvent
from actions.switch_action import SwitchAction

def event_filter(event):
    return event.button_name == "Basement Switch Button"


def register_callbacks():
    event_dispatcher.register_callback(on_button_clicked, ButtonClickEvent.__name__, event_filter=event_filter)
    
def on_button_clicked(event):
    if event.click_type == "single":
        on_single_click(event)
    elif event.click_type == "long_click_press":
        on_long_press(event)

def on_long_press(event):
    logger.info("Basement Button single clicked")

    hassutil.toggle(hassutil.Entity(name_map["Workout Mode"]))

def on_single_click(event):
    logger.info("Basement Button long press")

    SwitchAction().add_switches(["Basement Fan Switch", "Basement Treadmill Fan"]).toggle()
