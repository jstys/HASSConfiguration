import random
from util import hassutil

INTENT = "ColorIntent"

def initialize(api):
    pass

def handle(api, json_message, received_room, group_yaml, *args, **kwargs):
    room = json_message.get('Room')
    room = received_room if room is None else room.replace(" ", "_")
    color = json_message.get('Color')
    allMod = json_message.get('AllModifier') is not None

    device, device_type = hassutil.convert_device_information(json_message, ["LightObject", "LampObject"])
    devices = hassutil.get_devices_for_type(device_type, room, group_yaml)    

    if allMod:
        if device_type == "LightObject":
            for entity in devices:
                if "lamp" in entity.name or "light" in entity.name:
                    hassutil.turn_off_on(api, entity, True, color=color)
    else:
        for entity in devices:
            if device in entity.name:
                hassutil.turn_off_on(api, entity, True, color=color)