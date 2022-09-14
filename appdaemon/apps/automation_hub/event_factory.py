from util import logger
from util.entity_map import entity_map
from util.entity_map import button_id_map
from util.entity_map import nfc_tag_id_map
from util.entity_map import nfc_scanner_id_map
from util.entity_map import zwave_scene_map
from events.motion_triggered_event import MotionTriggeredEvent
from events.motion_cleared_event import MotionClearedEvent
from events.button_click_event import ButtonClickEvent
from events.door_closed_event import DoorClosedEvent
from events.door_open_event import DoorOpenEvent
from events.zwave_scene_event import ZwaveSceneEvent
from events.mqtt_event import MQTTEvent
from events.presence_event import PresenceEvent
from events.lock_event import LockEvent
from events.input_event import InputEvent
from events.generate_mealplan_event import GenerateMealplanEvent
from events.archive_mealplan_event import ArchiveMealplanEvent
from events.sunrise_event import SunriseEvent
from events.sunset_event import SunsetEvent
from events.switch_off_event import SwitchOffEvent
from events.switch_on_event import SwitchOnEvent
from events.nhl_goal_event import NHLGoalEvent
from events.nhl_penalty_event import NHLPenaltyEvent
from events.nhl_period_start_event import NHLPeriodStartEvent
from events.nhl_period_end_event import NHLPeriodEndEvent
from events.nhl_game_end_event import NHLGameEndEvent
from events.power_sensor_off_event import PowerSensorOffEvent
from events.power_sensor_on_event import PowerSensorOnEvent
from events.automation_hub_started_event import AutomationHubStartedEvent
from events.water_sensor_dry_event import WaterSensorDryEvent
from events.water_sensor_wet_event import WaterSensorWetEvent
from events.door_lock_notification_locked_event import DoorLockNotificationLockedEvent
from events.door_lock_notification_unlocked_event import DoorLockNotificationUnlockedEvent
from events.unavailable_event import UnavailableEvent
from events.available_event import AvailableEvent
from events.light_off_event import LightOffEvent
from events.light_on_event import LightOnEvent
from events.nfc_event import NFCEvent

def create_from_event(event_name, data, kwargs):
    if event_name == "xiaomi_aqara.click":
        return create_xiaomi_click_event(event_name, data, kwargs)
    elif event_name == "MQTT_MESSAGE":
        return create_mqtt_event(event_name, data, kwargs)
    elif event_name == "zwave_js_event" or event_name == "zwave_js_value_notification":
        return create_zwave_scene_event(event_name, data, kwargs)
    elif event_name == "generate_mealplan":
        return GenerateMealplanEvent()
    elif event_name == "archive_mealplan":
        return ArchiveMealplanEvent()
    elif event_name == "zha_event":
        return create_from_zha_event(event_name, data, kwargs)
    elif event_name == "nhl_scoring":
        return create_nhl_scoring_event(event_name, data, kwargs)
    elif event_name == "nhl_penalty":
        return create_nhl_penalty_event(event_name, data, kwargs)
    elif event_name == "nhl_period_start":
        return create_nhl_period_start_event(event_name, data, kwargs)
    elif event_name == "nhl_period_end":
        return create_nhl_period_end_event(event_name, data, kwargs)
    elif event_name == "nhl_game_end":
        return create_nhl_game_end_event(event_name, data, kwargs)
    elif event_name == "tag_scanned":
        return create_nfc_event(event_name, data, kwargs)

    logger.debug(f"Received invalid event type: {event_name}")
    return None

def create_from_zha_event(event_name, data, kwargs):
    command = data.get("command")
    if command == "click":
        unique_id = data.get("unique_id")
        if unique_id in button_id_map:
            friendly_name = button_id_map[unique_id]["name"]
            button_type = button_id_map[unique_id]['type']
            if button_type == 'lightify':
                command = data.get('commmand', 'on')
                click_type = 'unknown'
                if command == 'on':
                    click_type = 'single'
                elif command == 'move':
                    click_type = 'long'
                elif command == 'stop':
                    click_type = 'release'
                event = ButtonClickEvent()
                event.button_name = friendly_name
                event.click_type = click_type
                return event

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
        logger.warning(f"Received invalid click entity: {entity}")
        return None
        
def create_mqtt_event(event_name, data, kwargs):
    payload = data.get("payload")
    topic = data.get("topic")
    event = MQTTEvent()
    event.payload = payload
    event.topic = topic
    return event

def create_zwave_scene_event(event_name, data, kwargs):
    node_id = data.get("node_id")
    scene_id = data.get("property_key")
    if node_id in zwave_scene_map:
        event = ZwaveSceneEvent()
        event.name = zwave_scene_map[node_id]["name"]
        event.scene_id = int(scene_id)
        return event
    else:
        logger.warning(f"Received invalid zwave node_id: {node_id}")
        return None

def create_nhl_scoring_event(event_name, data, kwargs):
    event = NHLGoalEvent()
    event.team = data.get('team')
    
    scorer = data.get('scorer')
    event.scorer = scorer.get('name')
    event.scorer_number = scorer.get('number')
    
    assists = data.get('assists')
    if assists:
        for index, player in enumerate(assists):
            if index == 0:
                event.primary_assist = player.get('name')
                event.primary_number = player.get('number')
            elif index == 1:
                event.secondary_assist = player.get('name')
                event.secondary_number = player.get('number')

    return event

def create_nhl_penalty_event(event_name, data, kwargs):
    event = NHLPenaltyEvent()
    event.team = data.get('team')

    player = data.get('player')
    event.player = player.get('name')
    event.number = player.get('number')

    event.duration = data.get('duration')
    event.penalty = data.get('penalty')
    event.severity = data.get('severity')

    return event

def create_nhl_period_start_event(event_name, data, kwargs):
    event = NHLPeriodStartEvent()
    event.period = data.get('period')
    return event

def create_nhl_period_end_event(event_name, data, kwargs):
    event = NHLPeriodEndEvent()
    event.period = data.get('period')
    return event

def create_nhl_game_end_event(event_name, data, kwargs):
    return NHLGameEndEvent()
    
def create_automation_hub_started_event():
    return AutomationHubStartedEvent()

def create_nfc_event(event_name, data, kwargs):
    tag_id = data.get('tag_id')
    device_id = data.get('device_id')
    if not tag_id in nfc_tag_id_map:
        logger.warning(f"{tag_id} is not a recognized NFC tag")
        return None
    elif not device_id in nfc_scanner_id_map:
        logger.warning(f"{device_id} is not a recongized NFC scanner")
        return None

    return NFCEvent(tag_id=nfc_tag_id_map[tag_id], scanner_id=nfc_scanner_id_map[device_id])

def create_from_state_change(friendly_name, entity_type, entity, attributes, old, new, kwargs):
    adevents = []
    if old != new and new.lower() == "unavailable":
        adevents.append(create_unavailable_event(friendly_name))
    elif old != new and old.lower() == "unavailable":
        adevents.append(create_available_event(friendly_name))

    state_change_event = None
    if entity_type == "water_sensor":
        state_change_event = create_water_sensor_change_event(friendly_name, entity, attributes, old, new, kwargs)
    if entity_type == "motion_sensor":
        state_change_event = create_motion_sensor_state_change_event(friendly_name, entity, attributes, old, new, kwargs)
    if entity_type == "door_sensor":
        state_change_event = create_door_sensor_state_change_event(friendly_name, entity, attributes, old, new, kwargs)
    if entity_type == "presence":
        state_change_event = create_presence_change_event(friendly_name, entity, attributes, old, new, kwargs)
    if entity_type == "lock":
        state_change_event = create_lock_change_event(friendly_name, entity, attributes, old, new, kwargs)
    if entity_type in ["input_boolean", "input_select"]:
        state_change_event = create_input_change_event(friendly_name, entity, attributes, old, new, kwargs)
    if entity_type == "switch":
        state_change_event = create_switch_change_event(friendly_name, entity, attributes, old, new, kwargs)
    if friendly_name == "sun":
        state_change_event = create_sun_event(old, new)
    if entity_type == "binary_power_sensor":
        state_change_event = create_power_sensor_change_event(friendly_name, entity, attributes, old, new, kwargs)
    if friendly_name == "front_door_lock_alarmtype":
        state_change_event = create_door_lock_notification_event(friendly_name, entity, attributes, old, new, kwargs)
    if entity_type == "light":
        state_change_event = create_light_change_event(friendly_name, entity, attributes, old, new, kwargs)

    if state_change_event:
        adevents.append(state_change_event)
    else:
        logger.debug(f"Received invalid state change entity - type: {entity_type} entity: {friendly_name}")

    return adevents

def create_motion_sensor_state_change_event(friendly_name, entity, attributes, old, new, kwargs):
    if old != new and new == "off":
        logger.debug("Creating MotionClearedEvent")
        event = MotionClearedEvent()
        event.name = friendly_name
        return event
    elif old != new and new == "on":
        logger.debug("Creating MotionTriggeredEvent")
        event = MotionTriggeredEvent()
        event.name = friendly_name
        return event
    else:
        logger.warning("Received invalid motion state transition")
        return None

def create_door_sensor_state_change_event(friendly_name, entity, attributes, old, new, kwargs):
    if old != new and new == "on":
        logger.debug("Creating DoorOpenEvent")
        event = DoorOpenEvent()
        event.name = friendly_name
        return event
    elif old != new and new == "off":
        logger.debug("Creating DoorClosedEvent")
        event = DoorClosedEvent()
        event.name = friendly_name
        return event
    else:
        logger.warning("Received invalid door state transition")
        return None
        
def create_presence_change_event(friendly_name, entity, attributes, old, new, kwargs):
    logger.debug("Creating PresenceEvent")
    event = PresenceEvent()
    if old != new:
        event.name = friendly_name
        event.old = old
        event.new = new
        return event
    else:
        return None

def create_lock_change_event(friendly_name, entity, attributes, old, new, kwargs):
    logger.debug("Creating LockEvent")
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
    logger.debug("Creating InputEvent")
    if new != old:
        event = InputEvent()
        event.name = friendly_name
        event.old = old
        event.new = new
        return event
    else:
        logger.warning("Received invalid input transition")
        return None

def create_switch_change_event(friendly_name, entity, attributes, old, new, kwargs):
    logger.debug("Creating SwitchEvent")
    if old != new and new == "on":
        event = SwitchOnEvent()
        event.name = friendly_name
        return event
    elif old != new and new == "off":
        event = SwitchOffEvent()
        event.name = friendly_name
        return event
    else:
        logger.warning("Received invalid switch transition")
        return None

def create_light_change_event(friendly_name, entity, attributes, old, new, kwargs):
    logger.debug("Creating LightEvent")
    if old != new and new == "on":
        event = LightOnEvent()
        event.name = friendly_name
        return event
    elif old != new and new == "off":
        event = LightOffEvent()
        event.name = friendly_name
        return event
    else:
        logger.warning("Received invalid light transition")
        return None

def create_sun_event(old, new):
    logger.debug("Creating Sun event")
    if new != old and new == "above_horizon":
        return SunriseEvent()
    elif new != old and new == "below_horizon":
        return SunsetEvent()
        
def create_power_sensor_change_event(friendly_name, entity, attributes, old, new, kwargs):
    logger.debug("Creating Power Sensor Change Event")
    if old != new and new == "on":
        event = PowerSensorOnEvent()
        event.name = friendly_name
        return event
    elif old != new and new == "off":
        event = PowerSensorOffEvent()
        event.name = friendly_name
        return event
    else:
        logger.warning("Received invalid power sensor transition")
        return None

def create_water_sensor_change_event(friendly_name, entity, attributes, old, new, kwargs):
    logger.debug("Creating WaterSensorEvent")
    if old != new and new == "on":
        event = WaterSensorWetEvent()
        event.name = friendly_name
        return event
    elif old != new and new == "off":
        event = WaterSensorDryEvent()
        event.name = friendly_name
        return event
    else:
        logger.warning("Received invalid water sensor transition")
        return None

def create_door_lock_notification_event(friendly_name, entity, attributes, old, new, kwargs):
    logger.debug("Creating DoorLockNotificationEvent")
    if old != new and int(new) in [0x16, 0x13, 0x19]:
        event = DoorLockNotificationUnlockedEvent()
        event.name = friendly_name
        return event
    elif old != new and int(new) in [0x15, 0x12, 0x18]:
        event = DoorLockNotificationLockedEvent()
        event.name = friendly_name
        return event
    else:
        logger.warning("Received invalid door lock notification")
        return None

def create_unavailable_event(friendly_name):
    logger.debug("Creating UnavailableEvent")
    event = UnavailableEvent()
    event.name = friendly_name
    return event

def create_available_event(friendly_name):
    logger.debug("Creating AvailableEvent")
    event = AvailableEvent()
    event.name = friendly_name
    return event