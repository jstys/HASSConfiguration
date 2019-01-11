import yaml

file_contents = {}
entity_map = {}
name_map = {}
room_map = {}

def create_entity_and_name_maps():
    global entity_map
    global name_map
    
    if file_contents and "entities" in file_contents:
        for category, entities in file_contents.get("entities").items():
            for entity, attribs in entities.items():
                entity_map[entity] = attribs
                if "name" in attribs:
                    name_map[attribs["name"]] = entity
                elif "floor" in attribs:
                    name_map["{}_{}".format(attribs["floor"], category)] = entity
                else:
                    del entity_map[entity]
    
def create_room_map():
    global room_map
    
    if file_contents:
        room_map = file_contents.get("areas")

try:
    with open("entity_map.yaml") as yamlfile:
        file_contents = yaml.load(yamlfile)
except:
    file_contents = {}
    
create_entity_and_name_maps()
create_room_map()
