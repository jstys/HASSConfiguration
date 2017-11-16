#!/srv/homeassistant/bin/python3
import random

from util import hassutil

INTENT = "PowerIntent"

def handle(api, json_message, received_room, group_yaml):
    room = json_message.get('Room')
    room = received_room if room is None else room

    is_on_action = (json_message.get('PowerVerb') == "turn on")

    device = None
    deviceType = None
    for objectType in ["LightObject", "LampObject", "MediaObject", "InputName"]:
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
    if deviceType == "InputName":
        devices = [entity for entity in hassutil.get_tv_input_scripts(room, group_yaml)]
    elif room == "house":
        devices = [entity for entity in hassutil.get_all_switches_and_lights(group_yaml)]
    else:
        devices = [entity for entity in hassutil.get_group_switches_and_lights(room, group_yaml)]

    level = json_message.get('Percentage')
    allMod = json_message.get('AllModifier') is not None

    if allMod:
        if deviceType == "LightObject":
            hassutil.tts_say(api, random.choice(hassutil.AFFIRMATIVE_RESPONSES), tts_room=received_room)
            for entity in devices:
                if "lamp" in entity.name or "light" in entity.name:
                    hassutil.turn_off_on(api, entity, is_on_action, level)
    else:
        hassutil.tts_say(api, random.choice(hassutil.AFFIRMATIVE_RESPONSES), tts_room=received_room)
        for entity in devices:
            if device in entity.name:
                hassutil.turn_off_on(api, entity, is_on_action, level)
