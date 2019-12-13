from automation_hub import event_dispatcher
from automation_hub import state_machine
from util import logger
from events.sunrise_event import SunriseEvent
from events.sunset_event import SunsetEvent
from actions.light_action import LightAction
from actions.switch_action import SwitchAction

def register_callbacks():
    event_dispatcher.register_callback(on_sunrise, SunriseEvent.__name__)
    event_dispatcher.register_callback(on_sunset, SunsetEvent.__name__)
    
def on_sunrise(event):
    if state_machine.is_christmas_lights_enabled():
        SwitchAction().add_switches(["frontyard_outlet", "backyard_outlet", "porch_outlet"]).turn_off()
    LightAction().add_light("front_garden_lights").turn_off()

def on_sunset(event):
    if state_machine.is_christmas_lights_enabled():
        SwitchAction().add_switches(["frontyard_outlet", "backyard_outlet", "porch_outlet"]).turn_on()
    LightAction().add_light("front_garden_lights").turn_on()