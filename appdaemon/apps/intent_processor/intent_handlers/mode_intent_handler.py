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

    if allMod:
        if device_type == "LightObject":
            for entity in devices:
                if "lamp" in entity.name or "light" in entity.name:
                    hassutil.turn_off_on(api, entity, True, effect=mode)
    else:
        for entity in devices:
            if device in entity.name:
                hassutil.turn_off_on(api, entity, True, effect=mode)