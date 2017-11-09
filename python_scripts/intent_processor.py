#!/srv/homeassistant/bin/python3
import json
import sys
import hassutil
import homeassistant.remote as remote

BROADCAST_ROOM = "broadcast"

api = remote.API('127.0.0.1')
received_room = None

class Entity(object):
    def __init__(self, fully_qualified_name):
        fqn_split = fully_qualified_name.split(".")
        self.domain = fqn_split[0]
        self.name = fqn_split[1]
        self.entity_id = fully_qualified_name

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

    devices = []
    if room == "house":
        devices = [Entity(name) for name in hassutil.get_all_switches_and_lights()]
    else:
        devices = [Entity(name) for name in hassutil.get_group_switches_and_lights(room)]

    is_on_action = (json_message['PowerVerb'] == "turn on")

    device = None
    deviceType = None
    for objectType in ["LightObject", "LampObject", "MediaObject"]:
        try:
            device = json_message[objectType].lower().replace(" ", "_")
            deviceType = objectType
        except KeyError:
            continue

    if deviceType == "LightObject":
        device = "light"
    elif deviceType == "LampObject":
        device = "lamp"

    level = json_message.get('Percentage')
    allMod = json_message.get('AllModifier') is not None


    if allMod:
        if deviceType == "LightObject":
            tts_say("Okay")
            for entity in devices:
                if "lamp" in name or "light" in name:
                    turn_off_on(entity, is_on_action, level)
    else:
        tts_say("Okay")
        for entity in devices:
            if device in name:
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
