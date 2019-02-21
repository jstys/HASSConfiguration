from util import logger
from util.entity_map import entity_map
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from events.button_click_event import ButtonClickEvent
from events.door_closed_event import DoorClosedEvent
from events.door_open_event import DoorOpenEvent
from events.zwave_scene_event import ZwaveSceneEvent
from events.mqtt_event import MQTTEvent
from events.state_machine_event import StateMachineEvent
from events.presence_event import PresenceEvent
from events.lock_event import LockEvent
from events.input_event import InputEvent

def create_from_event(event_name, data, kwargs):
    if event_name == "xiaomi_aqara.click":
        return create_xiaomi_click_event(event_name, data, kwargs)
    elif event_name == "xiaomi_aqara.motion":
        return create_xiaomi_motion_event(event_name, data, kwargs)
    elif event_name == "MQTT_MESSAGE":
        return create_mqtt_event(event_name, data, kwargs)
    elif event_name == "zwave.scene_activated":
        return create_zwave_scene_event(event_name, data, kwargs)
    elif event_name == "state_machine.state_changed":
        return create_state_machine_state_changed_event(event_name, data, kwargs)

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
        
def create_xiaomi_motion_event(event_name, data, kwargs):
    entity = data.get("entity_id")
    if entity in entity_map:
        friendly_name = entity_map[entity]["name"]
        event = MotionTriggeredEvent()
        event.name = friendly_name
        return event
    else:
        logger.warning("Received invalid motion entity")
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

def create_state_machine_state_changed_event(event_name, data, kwargs):
    state = data.get("state")
    old = data.get("old")
    new = data.get("new")
    event = StateMachineEvent()
    event.state = state
    event.old = old
    event.new = new
    return event

def create_from_state_change(friendly_name, entity_type, entity, attributes, old, new, kwargs):
    if entity_type == "water_sensor":
        pass
    if entity_type == "motion_sensor":
        return create_motion_sensor_state_change_event(friendly_name, entity, attributes, old, new, kwargs)
    if entity_type == "door_sensor":
        return create_door_sensor_state_change_event(friendly_name, entity, attributes, old, new, kwargs)
    if entity_type == "presence":
        return create_presence_change_event(friendly_name, entity, attributes, old, new, kwargs)
    if entity_type == "lock":
        return create_lock_change_event(friendly_name, entity, attributes, old, new, kwargs)
    if entity_type in ["input_boolean", "input_select"]:
        return create_input_change_event(friendly_name, entity, attributes, old, new, kwargs)
    
    logger.warning("Received invalid state change entity")
    return None

def create_motion_sensor_state_change_event(friendly_name, entity, attributes, old, new, kwargs):
    if new == "off":
        logger.info("Creating MotionClearedEvent")
        event = MotionClearedEvent()
        event.name = friendly_name
        return event
    else:
        logger.warning("Received invalid motion state transition")
        return None

def create_door_sensor_state_change_event(friendly_name, entity, attributes, old, new, kwargs):
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
        
def create_presence_change_event(friendly_name, entity, attributes, old, new, kwargs):
    logger.info("Creating PresenceEvent")
    event = PresenceEvent()
    event.name = friendly_name
    event.old = old
    event.new = new
    return event

def create_lock_change_event(friendly_name, entity, attributes, old, new, kwargs):
    logger.info("Creating LockEvent")
    if new != old:
        event = LockEvent()
        event.name = friendly_name
        event.is_locked = True if new == "locked" else False
        event.status = attributes.get("lock_status")
        return event
    else:
        logger.warning("Received invalid lock transition")
        return None

def create_input_change_event(friendly_name, entity, attributes, old, new, kwargs):
    logger.info("Creating InputEvent")
    if new != old:
        event = InputEvent()
        event.name = friendly_name
        event.old = old
        event.new = new
        return event
    else:
        logger.warning("Received invalid input transition")
        return None