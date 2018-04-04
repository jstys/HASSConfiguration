import random
from util import hassutil

INTENT = "LevelIntent"

def handle(api, json_message, received_room, group_yaml, *args, **kwargs):
    room = json_message.get('Room')
    room = received_room if room is None else room
    level = json_message.get('Percentage')
    if level is None and "MaxVal" in json_message:
        level = "100"
    elif level is None and "MinVal" in json_message:
        level = "10"

    device = None
    deviceType = None
    for objectType in ["LightObject", "LampObject", "MediaObject"]:
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
            hassutil.tts_say(api, random.choice(hassutil.AFFIRMATIVE_RESPONSES), tts_room=received_room)
            for entity in devices:
                if "lamp" in entity.name or "light" in entity.name:
                    hassutil.set_level(api, entity, level)
    else:
        hassutil.tts_say(api, random.choice(hassutil.AFFIRMATIVE_RESPONSES), tts_room=received_room)
        for entity in devices:
            if device in entity.name:
                hassutil.set_level(api, entity, level)