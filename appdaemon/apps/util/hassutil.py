import yaml
import os

HASS_DIR = "/home/homeassistant/.homeassistant"
GROUPS = os.path.join(HASS_DIR, "groups.yaml")
SECRETS = os.path.join(HASS_DIR, "secrets.yaml")
BROADCAST_ROOM = "broadcast"
AFFIRMATIVE_RESPONSES = ["sure thing", "you got it", "as you wish", "no worries", "roger that"]

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

def get_tv_input_scripts(room, parsed_yaml):
    result = []

    group_entity = parsed_yaml.get(room)
    if group_entity is not None:
        for entity_id in group_entity['entities']:
            entity = Entity(entity_id)
            if entity.domain == "script" and "input" in entity.name:
                result.append(entity)
            elif entity.domain == "group":
                result.extend(get_tv_input_scripts(entity.name, parsed_yaml))

    return result

def get_all_switches_and_lights(parsed_yaml):
    result = []

    for name, group in parsed_yaml.items():
        for entity_name in group['entities']:
            entity = Entity(entity_name)
            if entity.domain == "switch" or entity.domain == "light":
                result.append(entity)

    return result

def get_group_switches_and_lights(group, parsed_yaml):
    result = []

    group_entity = parsed_yaml.get(group)
    if group_entity is not None:
        for entity_name in group_entity['entities']:
            entity = Entity(entity_name)
            if entity.domain in ["light", "switch"]:
                result.append(entity)
            elif entity.domain == "group":
                result.extend(get_group_switches_and_lights(entity.name, parsed_yaml))

    return result

def gui_notify(api, title, message):
    call_service(api, "persistent_notification", "create", title=title, message=message)

def pushbullet_notify(api, account, devices, title, message):
    call_service(api, "notify", account, title=title, message=message, target=devices)

def tts_say(api, message, tts_room):
    call_service(api, "script", "assistant_voice", message=message, room=tts_room)

def tts_broadcast(api, message, source="HASS"):
    call_service(api, "script", "assistant_broadcast", message=message, source=source)

def turn_off_on(api, entity, on, brightness=None, color=None, effect=None):
    brightness = 75 if brightness is None else brightness.replace("%", "")
    color = "white" if color is None else color
    if on:
        if entity.domain == "light":
            api.turn_on(entity.entity_id, brightness_pct=brightness, color_name=color, effect=effect)
        else:
            api.turn_on(entity.entity_id)
    else:
        api.turn_off(entity.entity_id)

def call_service(api, domain, action, **kwargs):
    api.call_service("/".join([domain, action]), **kwargs)
