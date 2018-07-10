#!/srv/homeassistant/bin/python3
import random

from util import hassutil

INTENT = "PowerIntent"

def initialize(api):
    pass

def handle(api, json_message, received_room, group_yaml, *args, **kwargs):
    room = json_message.get('Room')
    room = received_room if room is None else room.replace(" ", "_")
    level = json_message.get('Percentage')
    allMod = json_message.get('AllModifier') is not None
    is_on_action = (json_message.get('PowerVerb') == "turn on")

    device, device_type = hassutil.convert_device_information(json_message, ["LightObject", "LampObject", "MediaObject", "InputName", "ACObject"])
    devices = hassutil.get_devices_for_type(device_type, room, group_yaml)

    if allMod:
        if device_type == "LightObject":
            hassutil.tts_say(api, random.choice(hassutil.AFFIRMATIVE_RESPONSES), tts_room=received_room)
            for entity in devices:
                if "lamp" in entity.name or "light" in entity.name:
                    hassutil.turn_off_on(api, entity, is_on_action, level)
    else:
        hassutil.tts_say(api, random.choice(hassutil.AFFIRMATIVE_RESPONSES), tts_room=received_room)
        for entity in devices:
            if device in entity.name:
                hassutil.turn_off_on(api, entity, is_on_action, level)
