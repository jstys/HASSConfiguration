import random
from util import hassutil

INTENT = "LevelIntent"

def handle(api, json_message, received_room, group_yaml, *args, **kwargs):
    room = json_message.get('Room')
    room = received_room if room is None else room.replace(" ", "_")
    level = json_message.get('Percentage')
    if level is None and "MaxVal" in json_message:
        level = "100"
    elif level is None and "MinVal" in json_message:
        level = "10"

    device, device_type = hassutil.convert_device_information(json_message, ["LightObject", "LampObject", "MediaObject"])
    devices = hassutil.get_devices_for_type(device_type, room, group_yaml)

    allMod = json_message.get('AllModifier') is not None

    if allMod:
        if device_type == "LightObject":
            hassutil.tts_say(api, random.choice(hassutil.AFFIRMATIVE_RESPONSES), tts_room=received_room)
            for entity in devices:
                if "lamp" in entity.name or "light" in entity.name:
                    hassutil.set_level(api, entity, level)
    else:
        hassutil.tts_say(api, random.choice(hassutil.AFFIRMATIVE_RESPONSES), tts_room=received_room)
        for entity in devices:
            if device in entity.name:
                hassutil.set_level(api, entity, level)