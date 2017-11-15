import yaml
import os

HASS_DIR = "/home/homeassistant/.homeassistant"
GROUPS = "groups.yaml"

class Entity(object):
    def __init__(self, fully_qualified_name):
        fqn_split = fully_qualified_name.split(".")
        self.domain = fqn_split[0].strip()
        self.name = fqn_split[1].strip()
        self.entity_id = fully_qualified_name

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
