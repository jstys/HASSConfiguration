import yaml
import os

HASS_DIR = "/home/homeassistant/.homeassistant"
GROUPS = os.path.join(HASS_DIR, "groups.yaml")
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

class Entity(object):
    def __init__(self, fully_qualified_name):
        fqn_split = fully_qualified_name.split(".")
        self.domain = fqn_split[0].strip()
        self.name = fqn_split[1].strip()
        self.entity_id = fully_qualified_name

    @classmethod
    def fromSplitName(cls, domain, name):
        return cls(".".join([domain, name]))

def read_config_file(filename):
    try:
        with open(filename) as yamlfile:
            return yaml.load(yamlfile)
    except:
        return {}

def gui_notify(api, title, message):
    call_service(api, "persistent_notification", "create", title=title, message=message)

def pushbullet_notify(api, account, devices, title, message):
    call_service(api, "notify", account, title=title, message=message, target=devices)

def tts_say(api, message, tts_room):
    call_service(api, "script", "assistant_voice", message=message, room=tts_room)

def tts_broadcast(api, message, source="HASS"):
    call_service(api, "script", "assistant_broadcast", message=message, source=source)

def turn_off_on(api, entity, on, brightness=None, color=None, effect=None):
    optionals = {}
    if effect is not None:
        optionals["effect"] = effect
    else:
        optionals["brightness_pct"] = 75 if brightness is None else brightness.replace("%", "")
        optionals["color_name"] = "white" if color is None else color
    if on:
        if entity.domain == "light":
            api.turn_on(entity.entity_id, **optionals)
        else:
            api.turn_on(entity.entity_id)
    else:
        api.turn_off(entity.entity_id)
        
def set_level(api, entity, percentage):
    if entity.domain == "light":
        api.turn_on(entity.entity_id, brightness_pct=percentage.replace("%", ""))

def call_service(api, domain, action, **kwargs):
    api.call_service("/".join([domain, action]), **kwargs)

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
            if OBJECT_MAP.get(device_type) in entity.name:
                result.append(entity)
            elif entity.domain == "group":
                result.extend(_get_devices_for_type_in_group(device_type, entity.name, parsed_yaml))

    return result