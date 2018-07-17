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

    # hassutil.tts_say(api, random.choice(hassutil.AFFIRMATIVE_RESPONSES), tts_room=received_room)
    for entity in devices:
        hassutil.turn_off_on(api, entity, True, color=color)