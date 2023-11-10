import event_dispatcher
import state_machine
from util import logger
from events.sunrise_event import SunriseEvent
from events.sunset_event import SunsetEvent
from actions.light_action import LightAction
from actions.switch_action import SwitchAction

def register_callbacks():
    event_dispatcher.register_callback(on_sunrise, SunriseEvent.__name__)
    event_dispatcher.register_callback(on_sunset, SunsetEvent.__name__)
    
def on_sunrise(event):
    if state_machine.is_enabled("Christmas Lights Mode"):
        SwitchAction().add_switches(["Frontyard Outlet", "Backyard Outlet", "Porch Outlet"]).turn_off()

def on_sunset(event):
    if state_machine.is_enabled("Christmas Lights Mode"):
        SwitchAction().add_switches(["Frontyard Outlet", "Backyard Outlet", "Porch Outlet"]).turn_on()