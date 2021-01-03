import event_dispatcher
from util import logutil
from events.water_sensor_wet_event import WaterSensorWetEvent
from events.water_sensor_dry_event import WaterSensorDryEvent
from actions.push_notify_action import PushNotifyAction

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name == "utility_room_water_sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_water_event, WaterSensorWetEvent.__name__, event_filter=event_filter)
    event_dispatcher.register_callback(on_water_event, WaterSensorDryEvent.__name__, event_filter=event_filter)    

def on_water_event(event):
    if isinstance(event, WaterSensorWetEvent):
        on_wet_event(event)
    elif isinstance(event, WaterSensorDryEvent):
        on_dry_event(event)

def on_wet_event(event):
    logger.info("Basement sensor wet")

    PushNotifyAction().add_target("jim_cell").set_message("Basement wet!").notify()

def on_dry_event(event):
    logger.info("Basement sensor dry")

    PushNotifyAction().add_target("jim_cell").set_message("Basement dry!").notify()
