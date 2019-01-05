import logger
from util.entity_map import entity_map
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from events.button_click_event import ButtonClickEvent
from events.door_closed_event import DoorClosedEvent
from events.door_open_event import DoorOpenEvent

def create_from_event(event_name, data, kwargs):
    if event_name == "click":
        return create_click_event(event_name, data, kwargs)

    return None

def create_click_event(event_name, data, kwargs):
    click_type = data.get("click_type")
    entity = data.get("entity_id")
    if entity in entity_map:
        friendly_name = entity_map[entity]["name"]
        event = ButtonClickEvent()
        event.button_name = friendly_name
        event.click_type = click_type
        return event
    else:
        return None

def create_from_state_change(friendly_name, entity_type, entity, attribute, old, new, kwargs):
    if entity_type == "water_sensor":
        pass
    if entity_type == "motion_sensor":
        return create_motion_sensor_state_change_event(friendly_name, entity, attribute, old, new, kwargs)
    if entity_type == "door_sensor":
        return create_door_sensor_state_change_event(friendly_name, entity, attribute, old, new, kwargs)
    if entity_type == "device_tracker":
        pass
    
    return None
    
def create_motion_sensor_state_change_event(friendly_name, entity, attribute, old, new, kwargs):
    if old == "off" and new == "on":
        logger.info("Creating MotionTriggeredEvent")
        event = MotionTriggeredEvent()
        event.name = friendly_name
        return event
    elif old == "on" and new == "off":
        logger.info("Creating MotionClearedEvent")
        event = MotionClearedEvent()
        event.name = friendly_name
        return event
    else:
        return None

def create_door_sensor_state_change_event(friendly_name, entity, attribute, old, new, kwargs):
    if old == "off" and new == "on":
        logger.info("Creating DoorOpenEvent")
        event = DoorOpenEvent()
        event.name = friendly_name
        return event
    elif old == "on" and new == "off":
        logger.info("Creating DoorClosedEvent")
        event = DoorClosedEvent()
        event.name = friendly_name
        return event
    else:
        return None