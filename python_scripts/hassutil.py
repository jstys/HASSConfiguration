import yaml
import os

HASS_DIR = "/home/homeassistant/.homeassistant"
GROUPS = "groups.yaml"

def read_config_file(filename):
    try:
        with open(filename) as yamlfile:
            return yaml.load(yamlfile)
    except:
        return {}

def get_all_switches_and_lights():
    result = []
    parsed_yaml = read_config_file(os.path.join(HASS_DIR, GROUPS))

    for name, group in parsed_yaml.items():
        for entity in group['entities']:
            entity_split = entity.split('.')
            domain = entity_split[0]
            name = entity_split[1]
            if domain == "switch" or domain == "light":
                result.append(entity)

    return result

def get_group_switches_and_lights(group):
    result = []
    parsed_yaml = read_config_file(os.path.join(HASS_DIR, GROUPS))

    group_entity = parsed_yaml.get(group)
    if group_entity is not None:
        for entity in group_entity['entities']:
            entity_split = entity.split('.')
            domain = entity_split[0]
            name = entity_split[1]
            if domain == "switch" or domain == "light":
                result.append(entity)
            elif domain == "group":
                result.extend(get_group_switches_and_lights(name))

    return result
