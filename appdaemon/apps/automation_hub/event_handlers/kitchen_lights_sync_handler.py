import event_dispatcher
from util import logutil
from events.light_on_event import LightOnEvent
from events.light_off_event import LightOffEvent
from actions.light_action import LightAction

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name == "kitchen_fixture"

def register_callbacks():
    event_dispatcher.register_callback(handle_turned_on, LightOnEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(handle_turned_off, LightOffEvent.__name__, event_filter=event_filter)

def handle_turned_on(event):
    LightAction().add_light("kitchen_hi_hats").turn_on()
    
def handle_turned_off(event):
    LightAction().add_light("kitchen_hi_hats").turn_off()
    