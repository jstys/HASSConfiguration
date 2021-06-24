import event_dispatcher
from util import logutil
from events.switch_on_event import SwitchOnEvent
from events.switch_off_event import SwitchOffEvent
from actions.light_action import LightAction

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name == "kitchen_fixture"

def register_callbacks():
    event_dispatcher.register_callback(handle_turned_on, SwitchOnEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(handle_turned_off, SwitchOffEvent.__name__, event_filter=event_filter)

def handle_turned_on(event):
    LightAction().add_light("kitchen_hi_hats").turn_on()
    
def handle_turned_off(event):
    LightAction().add_light("kitchen_hi_hats").turn_off()
    