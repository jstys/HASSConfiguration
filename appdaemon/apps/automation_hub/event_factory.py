from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent

def create_from_event(event_name, data, kwargs):
    return None

def create_from_state_change(friendly_name, entity_type, entity, attribute, old, new, kwargs):
    if entity_type == "water_sensor":
        pass
    if entity_type == "motion_sensor":
        return create_motion_sensor_state_change_event(friendly_name, entity, attribute, old, new, kwargs)
    if entity_type == "door_sensor":
        pass
    if entity_type == "xiaomi_button":
        pass
    if entity_type == "device_tracker":
        pass
    
    return None
    
def create_motion_sensor_state_change_event(friendly_name, entity, attribute, old, new, kwargs):
    if old == "off" and new == "on":
        event = MotionTriggeredEvent()
        event.name = friendly_name
        return event
    elif old == "on" and new == "off":
        event = MotionClearedEvent()
        event.name = friendly_name
        return event
    else:
        return None