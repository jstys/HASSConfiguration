import yaml
import os

import logger

HASS_DIR = "/home/homeassistant/.homeassistant"
GROUPS = os.path.join(HASS_DIR, "groups", "groups.yaml")
SECRETS = os.path.join(HASS_DIR, "secrets.yaml")
BROADCAST_ROOM = "broadcast"
AFFIRMATIVE_RESPONSES = ["sure thing", "you got it", "as you wish", "no worries", "roger that"]
OBJECT_MAP = {
    "LightObject": ["light", "lights", "hi_hats"],
    "LampObject": ["lamp", "lamps"],
    "ACObject": ["ac", "air_conditioner"],
    "MediaObject": ["tv", "speaker", "speakers", "smartcast"],
    "InputName": ["tv_input"]
}
API_HANDLE = None

class Entity(object):
    def __init__(self, fully_qualified_name):
        fqn_split = fully_qualified_name.split(".")
        self.domain = fqn_split[0].strip()
        self.name = fqn_split[1].strip()
        self.entity_id = fully_qualified_name

    @classmethod
    def fromSplitName(cls, domain, name):
        return cls(".".join([domain, name]))

def set_api_handle(handle):
    global API_HANDLE
    API_HANDLE = handle

def read_config_file(filename):
    try:
        with open(filename) as yamlfile:
            return yaml.load(yamlfile)
    except:
        return {}

def gui_notify(title, message):
    call_service("persistent_notification", "create", title=title, message=message)

def join_notify(target, message, title="Home Assistant"):
    call_service("notify", target, message=message, title=title)

def tts_say(message, tts_room):
    call_service("script", "assistant_voice", message=message, room=tts_room)

def tts_broadcast(message, source="HASS"):
    call_service("script", "assistant_broadcast", message=message, source=source)
    
def lock(lock_entity):
    call_service("lock", "lock", entity_id=lock_entity.entity_id)
    
def unlock(lock_entity):
    call_service("lock", "unlock", entity_id=lock_entity.entity_id)

def turn_on(entity, brightness_pct=100, color_temp=255):
    if API_HANDLE is not None:
        if entity.domain == "light":
            API_HANDLE.turn_on(entity.entity_id, brightness_pct=brightness_pct, color_temp=color_temp, namespace="hass")
        else:
            API_HANDLE.turn_on(entity.entity_id, namespace="hass")
    else:
        logger.error("API Handle is None")

def set_light_effect(entity, effect=None):
    if API_HANDLE is not None:
        if effect:
            API_HANDLE.turn_on(entity.entity_id, effect=effect, namespace="hass")
        else:
            logger.error("Missing effect")
    else:
        logger.error("API Handle is None")

def set_light_color(entity, color=None):
    if API_HANDLE:
        if color:
            API_HANDLE.turn_on(entity.entity_id, color_name=color, namespace="hass")
        else:
            logger.error("Missing color")
    else:
        logger.error("API Handle is None")

def turn_off(entity):
    if API_HANDLE:
        API_HANDLE.turn_off(entity.entity_id, namespace="hass")
    else:
        logger.error("API Handle is None")
        
def set_level(entity, brightness_pct):
    if API_HANDLE:
        if entity.domain == "light":
            API_HANDLE.turn_on(entity.entity_id, brightness_pct=brightness_pct.replace("%", ""), namespace="hass")
        else:
            logger.error("Can't set level on non-light entity")
    else:
        logger.error("API Handle is None")

def call_service(domain, action, **kwargs):
    if API_HANDLE:
        API_HANDLE.call_service("/".join([domain, action]), namespace="hass", **kwargs)
    else:
        logger.error("API Handle is None")

def fire_event(event, **kwargs):
    if API_HANDLE:
        API_HANDLE.fire_event(event, namespace="hass", **kwargs)
    else:
        logger.error("API Handle is None")

def convert_device_information(intent_json, allowed_object_types):
    device = None
    device_type = None
    for object_type in allowed_object_types:
        try:
            device = intent_json[object_type].lower().replace(" ", "_")
            device_type = object_type
        except KeyError:
            device = None
            device_type = None
            continue
        else:
            break

    if device_type == "LightObject":
        device = "light"
    elif device_type == "LampObject":
        device = "lamp"
    elif device_type == "ACObject":
        device = "ac"

    return device, device_type

def get_devices_for_type(device_type, room, groups):
    devices = []
    if room == "house":
        for name, _ in groups.items():
            devices.extend(_get_devices_for_type_in_group(device_type, name, groups))
    else:
        devices = _get_devices_for_type_in_group(device_type, room, groups)

    return devices

def _get_devices_for_type_in_group(device_type, group, parsed_yaml):
    result = []
    if device_type not in OBJECT_MAP:
        return []

    group_entity = parsed_yaml.get(group)
    if group_entity is not None:
        for entity_name in group_entity['entities']:
            entity = Entity(entity_name)
            if entity.domain == "group":
                result.extend(_get_devices_for_type_in_group(device_type, entity.name, parsed_yaml))
            elif _is_matched_device_for_type(device_type, entity):
                result.append(entity)

    return result

def _is_matched_device_for_type(device_type, entity):
    for identifier in OBJECT_MAP.get(device_type):
        if identifier in entity.name:
            return True
    return False