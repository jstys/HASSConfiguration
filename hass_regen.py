import yaml
import re
import os
import sys

def name_to_friendly_name(name):
    return " ".join([string.capitalize() for string in name.split("_")])

customized = {}
entity_map = {}
template_files = {
    "hass/template/climate.yaml": "hass/climate.yaml",
    "hass/template/sensor/battery.yaml": "hass/sensor/battery.yaml",
    "hass/template/media_player/universal.yaml": "hass/media_player/universal.yaml",
    "hass/template/light/lightgroups.yaml": "hass/light/lightgroups.yaml",
    "hass/template/light/switches.yaml": "hass/light/switches.yaml",
    "hass/template/logbook.yaml" : "hass/logbook.yaml",
    "hass/template/binary_sensor/appliance.yaml": "hass/binary_sensor/appliance.yaml",
    "hass/template/cover/template.yaml": "hass/cover/template.yaml",
    "hass/template/scenes.yaml": "hass/scenes.yaml"
}

with open("entity_map.yaml", "r") as yamlfile:
    entity_map = yaml.safe_load(yamlfile)

with open("hass/customize.yaml", "r") as customization:
    customized = yaml.safe_load(customization)

entity_name_map = {}
for entity_type, entity_dict in entity_map["entities"].items():
    for entity_id, values in entity_dict.items():
        if "name" in values:
            entity_name_map[values["name"]] = entity_id
        elif "room" in values:
            room = values["room"]
            name = f"{room}_{entity_type}"
            entity_name_map[name] = entity_id

for entity_name, entity_id in entity_name_map.items():
    if entity_id in customized:
        customized[entity_id]["friendly_name"] = name_to_friendly_name(entity_name)
    elif entity_id not in customized:
        customized[entity_id] = {}
        customized[entity_id]["friendly_name"] = name_to_friendly_name(entity_name)

with open("hass/customize.yaml", "w") as customization:
    yaml.dump(customized, customization, default_flow_style=False)
    
for template, replacement in template_files.items():
    if not os.path.isfile(template):
        print(f"Couldn't find file: {template}")
        sys.exit(1)
        
    with open(template, "r") as templatefile:
        os.makedirs(os.path.dirname(replacement), exist_ok=True)
        with open(replacement, "w", newline="\n") as replacementfile:
            for line in templatefile.readlines():
                matches = re.findall(r"em:[a-zA-Z0-9_]+", line)
                subbed_line = line
                for match in matches:
                    entity_name = match.split(":")[1]
                    if entity_name not in entity_name_map:
                        print(f"Unable to find entity_name {entity_name}")
                        sys.exit(1)
                    entity_id = entity_name_map[entity_name]
                    subbed_line = subbed_line.replace(match, entity_id)
                replacementfile.write(subbed_line)
                    
    
        
