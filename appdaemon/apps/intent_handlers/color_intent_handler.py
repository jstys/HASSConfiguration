import random
from util import hassutil

INTENT = "ColorIntent"

def handle(api, json_message, received_room, group_yaml, *args, **kwargs):
    room = json_message.get('Room')
    room = received_room if room is None else room
    color = json_message.get('Color')

    device = None
    deviceType = None
    for objectType in ["LightObject", "LampObject"]:
        try:
            device = json_message[objectType].lower().replace(" ", "_")
            deviceType = objectType
        except KeyError:
            device = None
            deviceType = None
            continue
        else:
            break

    if deviceType == "LightObject":
        device = "light"
    elif deviceType == "LampObject":
        device = "lamp"

    devices = []
    if room == "house":
        devices = [entity for entity in hassutil.get_all_switches_and_lights(group_yaml)]
    else:
        devices = [entity for entity in hassutil.get_group_switches_and_lights(room, group_yaml)]

    allMod = json_message.get('AllModifier') is not None

    if allMod:
        if deviceType == "LightObject":
            for entity in devices:
                if "lamp" in entity.name or "light" in entity.name:
                    hassutil.turn_off_on(api, entity, True, color=color)
    else:
        for entity in devices:
            if device in entity.name:
                hassutil.turn_off_on(api, entity, True, color=color)