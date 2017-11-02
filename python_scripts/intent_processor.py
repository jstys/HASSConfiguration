#!/srv/homeassistant/bin/python3
import json
import sys
import homeassistant.remote as remote

BROADCAST_ROOM = "broadcast"

api = remote.API('127.0.0.1')
received_room = None

def handle_json_request(json_message):
    intent = json_message['intent_type']
    if intent == "PowerIntent":
        handle_power_intent(json_message)
    elif intent == "MediaIntent":
        tts_say("Sorry, I can't control media yet")
    elif intent == "BrightnessIntent":
        tts_say("Sorry, I can't control brightness yet")
    elif intent == "BroadcastIntent" or intent == "TalkIntent":
        tts_say("Sorry, I can't broadcast messages yet")
    elif intent == "ListIntent":
        tts_say("Sorry, I can't manage your lists yet")
    else:
        tts_say("Sorry, I don't understand what you're asking")

def handle_power_intent(json_message):
    action = (json_message['PowerVerb'].replace("turn ", ""))
    device = json_message['PowerableObject']
    tts_say("Turning {} the {}".format(action, device['value']['value']))

def tts_say(message, tts_room=received_room):
    if received_room == BROADCAST_ROOM:
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
