from automation_hub import event_dispatcher
from automation_hub import state_machine
from util import logger
from events.sunrise_event import SunriseEvent
from events.sunset_event import SunsetEvent

def register_callbacks():
    event_dispatcher.register_callback(on_sunrise, SunriseEvent.__name__)
    event_dispatcher.register_callback(on_sunset, SunsetEvent.__name__)
    
def on_sunrise(event):
    state_machine.set_state(state_machine.SUN_UP_STATE, True)
    state_machine.set_state(state_machine.SLEEP_STATE, False)

def on_sunset(event):
    state_machine.set_state(state_machine.SUN_UP_STATE, False)