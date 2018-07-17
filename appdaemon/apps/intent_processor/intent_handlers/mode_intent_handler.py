import random
from util import hassutil

INTENT = "ModeIntent"
MODES = {
    "disco": "Disco",
    "strobe": "Strobe epilepsy!",
    "color strobe": "Strobe color",
    "christmas": "Christmas",
    "color changing": "Slowdown",
    "police": "Police",
    "alarm": "Alarm"
}

def initialize(api):
    pass

def handle(api, json_message, received_room, group_yaml, *args, **kwargs):
    room = json_message.get('Room')
    room = received_room if room is None else room.replace(" ", "_")
    allMod = json_message.get('AllModifier') is not None
    mode = json_message.get('ModeName')
    mode = MODES.get(mode)
    if mode is None:
        return

    device, device_type = hassutil.convert_device_information(json_message, ["LightObject", "LampObject"])
    devices = hassutil.get_devices_for_type(device_type, room, group_yaml)

    # hassutil.tts_say(api, random.choice(hassutil.AFFIRMATIVE_RESPONSES), tts_room=received_room)
    for entity in devices:
        hassutil.turn_off_on(api, entity, True, effect=mode)