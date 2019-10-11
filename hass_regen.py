import yaml

entity_map = {}
templates_files = {
    "hass/template/ui-lovelace.yaml": "hass/ui-lovelace.yaml"
    "hass/template/sensor/battery.yaml": "hass/sensor/battery.yaml",
    "hass/template/media_player/universal.yaml": "hass/media_player/universal.yaml"
}

with open("entity_map.yaml", "r") as yamlfile:
    entity_map = yaml.load(yamlfile)

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
    print(f"{entity_name}: {entity_id}")
