from automation_hub import event_dispatcher
from automation_hub import logger
from events.button_click_event import ButtonClickEvent

def event_filter(event):
    return event.button_name == "living_room_button"

def register_callbacks():
    event_dispatcher.register_callback(on_button_clicked, ButtonClickEvent.__name__, event_filter=event_filter)
    
def on_button_clicked(event):
    if event.click_type == "single":
        on_single_click(event)
    elif event.click_type == "double":
        on_double_click(event)
    elif event.click_type == "long_click_press":
        on_long_press(event)

def on_single_click(event):
    logger.info("Living Room Button single clicked")

def on_double_click(event):
    logger.info("Living Room Button double clicked")

def on_long_press(event):
    logger.info("Living Room Button long pressed")
