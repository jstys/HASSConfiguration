#!/srv/homeassistant/bin/python3
import random

from util import hassutil

INTENT = "TalkIntent"

def handle(api, json_message, received_room):
    raw_message = json_message.get('raw')
    destination_room = json_message.get('Room')
    room_index = raw_message.find(destination_room)
    room_len = len(destination_room)
    actual_message = " ".join(["the", destination_room, "says", raw_message[(room_index + room_len + 1):]])

    if destination_room == "house":
        api.log("Broadcasting {} from {}".format(actual_message, received_room))
        hassutil.tts_broadcast(api, actual_message, source=received_room)
    else:
        api.log("Saying {} in {}".format(actual_message, destination_room))
        hassutil.tts_say(api, actual_message, destination_room.replace(" ", "_"))

