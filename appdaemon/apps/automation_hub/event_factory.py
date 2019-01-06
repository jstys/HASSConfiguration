from util import logger
from util.entity_map import entity_map
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from events.button_click_event import ButtonClickEvent
from events.door_closed_event import DoorClosedEvent
from events.door_open_event import DoorOpenEvent
from events.zwave_scene_event import ZwaveSceneEvent
from events.mqtt_event import MQTTEvent

def create_from_event(event_name, data, kwargs):
    if event_name == "xiaomi_aqara.click":
        return create_xiaomi_click_event(event_name, data, kwargs)
    elif event_name == "MQTT_MESSAGE":
        return create_mqtt_event(event_name, data, kwargs)
    elif event_name == "zwave.scene_activated":
        return create_zwave_scene_event(event_name, data, kwargs)

    logger.warning("Received invalid event type")
    return None

def create_xiaomi_click_event(event_name, data, kwargs):
    click_type = data.get("click_type")
    entity = data.get("entity_id")
    if entity in entity_map:
        friendly_name = entity_map[entity]["name"]
        event = ButtonClickEvent()
        event.button_name = friendly_name
        event.click_type = click_type
        return event
    else:
        logger.warning("Received invalid click entity")
        return None
        
def create_mqtt_event(event_name, data, kwargs):
    payload = data.get("payload")
    topic = data.get("topic")
    event = MQTTEvent()
    event.payload = payload
    event.topic = topic
    return event

def create_zwave_scene_event(event_name, data, kwargs):
    entity = data.get("entity_id")
    scene_id = data.get("scene_id")
    scene_data = data.get("scene_data")
    if entity in entity_map:
        event = ZwaveSceneEvent()
        event.name = entity_map[entity]["name"]
        event.scene_id = scene_id
        event.scene_data = scene_data
        return event
    else:
        logger.warning("Received invalid zwave entity")
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
    
    logger.warning("Received invalid state change entity")
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
        logger.warning("Received invalid motion state transition")
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
        logger.warning("Received invalid door state transition")
        return None