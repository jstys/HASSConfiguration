#!/srv/homeassistant/bin/python3
import json
import sys
import homeassistant.remote as remote

api = remote.API('127.0.0.1')
room = None

def handle_json_request(json_message):
    intent = json_message['intent']['intentName']
    if intent == "ActivateObject":
        handle_activate_deactivate_object(json_message, True)
    elif intent == "DeactivateObject":
        handle_activate_deactivate_object(json_message, False)
    elif intent == "ActivateLightColor":
        tts_say("Sorry, I can't do that yet")
    else:
        tts_say("Sorry, I don't understand what you're asking for")

def handle_activate_deactivate_object(json_message, activate):
    devices = [device for device in json_message.get('slots') if device['entity'] == "objectType"]
    for device in devices:
        action = "on" if activate else "off"
        tts_say("Turning {} {}".format(action, device['value']['value']))


def tts_say(message):
    remote.call_service(api, "script", "snips_voice", {"message": message, "room": room})

if __name__ == '__main__':
    topic = sys.argv[1]
    raw_payload = sys.argv[2]

    with open('/tmp/snips_input.txt', 'w') as debug_file:
        debug_file.write(raw_payload)

    json_payload = {}
    try:
        json_payload = json.loads(raw_payload)
    except:
        tts_say("Unable to parse request")
        sys.exit(1)

    room = topic.split("/")[1]

    tts_say("Received command from {} snips".format(room.replace("_", " ")))
    handle_json_request(json_payload)
