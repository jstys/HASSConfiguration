#!/srv/homeassistant/bin/python3
import json
import sys
import random
import hassutil
from hassutil import Entity
import homeassistant.remote as remote

BROADCAST_ROOM = "broadcast"
AFFIRMATIVE_RESPONSES = ["sure thing", "you got it", "as you wish", "no worries", "roger that"]

api = remote.API('127.0.0.1')
received_room = None

def handle_json_request(json_message):
    intent = json_message['intent_type']
    if intent == "PowerIntent":
        handle_power_intent(json_message)
    elif intent == "MediaIntent":
        tts_say("Sorry, I can't control media yet")
    elif intent == "LevelIntent":
        tts_say("Sorry, I can't control device levels yet")
    elif intent == "BroadcastIntent" or intent == "TalkIntent":
        tts_say("Sorry, I can't broadcast messages yet")
    elif intent == "ListIntent":
        tts_say("Sorry, I can't manage your lists yet")
    elif intent == "SceneIntent":
        tts_say("Actually, it's fuckin not")
    else:
        tts_say("Sorry, I don't understand what you're asking")

def handle_power_intent(json_message):
    room = json_message.get('Room')
    room = received_room if room is None else room

    is_on_action = (json_message['PowerVerb'] == "turn on")

    device = None
    deviceType = None
    for objectType in ["LightObject", "LampObject", "MediaObject", "InputName"]:
        try:
            device = json_message[objectType].lower().replace(" ", "_")
            deviceType = objectType
        except KeyError:
            continue

    if deviceType == "LightObject":
        device = "light"
    elif deviceType == "LampObject":
        device = "lamp"

    devices = []
    if deviceType == "InputName":
        devices = [entity for entity in hassutil.get_tv_input_scripts(room)]
    elif room == "house":
        devices = [entity for entity in hassutil.get_all_switches_and_lights()]
    else:
        devices = [entity for entity in hassutil.get_group_switches_and_lights(room)]

    level = json_message.get('Percentage')
    allMod = json_message.get('AllModifier') is not None


    if allMod:
        if deviceType == "LightObject":
            tts_say(random.choice(AFFIRMATIVE_RESPONSES))
            for entity in devices:
                if "lamp" in entity.name or "light" in entity.name:
                    turn_off_on(entity, is_on_action, level)
    else:
        tts_say(random.choice(AFFIRMATIVE_RESPONSES))
        for entity in devices:
            if device in entity.name:
                turn_off_on(entity, is_on_action, level)

def turn_off_on(entity, on, brightness):
    brightness = 75 if brightness is None else brightness.replace("%", "")
    if on:
        if entity.domain == "light":
            remote.call_service(api, entity.domain, "turn_on", {"entity_id": entity.entity_id, "brightness_pct": brightness})
        else:
            remote.call_service(api, entity.domain, "turn_on", {"entity_id": entity.entity_id})
    else:
        remote.call_service(api, entity.domain, "turn_off", {"entity_id": entity.entity_id})

def log(message):
    remote.call_service(api, "logbook", "log", {"name": "intent_processor.py", "message": message})

def tts_say(message, tts_room=None):
    tts_room = received_room if tts_room is None else tts_room
    if tts_room == BROADCAST_ROOM:
        remote.call_service(api, "script", "assistant_broadcast", {"message": message, "source": received_room})
    else:
        remote.call_service(api, "script", "assistant_voice", {"message": message, "room": tts_room})

if __name__ == '__main__':
    topic = sys.argv[1]
    raw_payload = sys.argv[2]

    json_payload = {}
    try:
        json_payload = json.loads(raw_payload)
        received_room = topic.split("/")[1]
    except:
        tts_say("Sorry, I'm unable to understand your request")
        sys.exit(1)

    handle_json_request(json_payload)
