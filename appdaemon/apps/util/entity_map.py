import yaml
from hassutil import read_config_file, ENTITY_MAP

file_contents = {}
entity_map = {}
name_map = {}
room_map = {}
assistant_list = []
button_id_map = {}
join_targets = []

def create_entity_and_name_maps(file_contents):
    global entity_map
    global name_map
    
    if file_contents and "entities" in file_contents:
        for category, entities in file_contents.get("entities").items():
            for entity, attribs in entities.items():
                attribs["type"] = category
                entity_map[entity] = attribs
                if "name" in attribs:
                    name_map[attribs["name"]] = entity
                elif "room" in attribs:
                    name = "{}_{}".format(attribs["room"], category)
                    entity_map[entity]["name"] = name
                    name_map[name] = entity
                else:
                    del entity_map[entity]
    
def create_room_map(file_contents):
    global room_map
    
    if file_contents:
        room_map = file_contents.get("areas")
        
def create_assistant_list(file_contents):
    global assistant_list
    
    if file_contents:
        assistant_list = file_contents.get("assistants")
        
def create_join_targets(file_contents):
    global join_targets
    
    if file_contents:
        join_targets = file_contents.get("join_targets")

def create_button_id_map(file_contents):
    global button_id_map

    if file_contents:
        button_id_map = file_contents.get("button_ids")
        
def find_type_entities(entity_type):
    matches = []
    for _, attribs in entity_map.items():
        if attribs.get("type") == entity_type:
            matches.append(attribs.get("name"))

    return matches

def find_room_entities(entity_type, room):
    matches = []
    for _, attribs in entity_map.items():
        if attribs.get("room") == room and attribs.get("type") == entity_type:
            matches.append(attribs.get("name"))

    return matches

file_contents = read_config_file(ENTITY_MAP)
    
create_entity_and_name_maps(file_contents)
create_room_map(file_contents)
create_assistant_list(file_contents)
create_join_targets(file_contents)
create_button_id_map(file_contents)