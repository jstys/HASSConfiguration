import yaml
from hassutil import read_config_file, ENTITY_MAP

file_contents = {}
entity_map = {}
name_map = {}
room_map = {}

def create_entity_and_name_maps(file_contents):
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
    
def create_room_map(file_contents):
    global room_map
    
    if file_contents:
        room_map = file_contents.get("areas")

file_contents = read_config_file(ENTITY_MAP)
    
create_entity_and_name_maps(file_contents)
create_room_map(file_contents)
