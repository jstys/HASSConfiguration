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
        tts_say("Sorry, I can't activate light colors yet")
    elif intent == "user_Q52Q01Nyv__ResumeDevice":
        handle_pause_resume_device(json_message, False)
    elif intent == "user_Q52Q01Nyv__PauseDevice":
        handle_pause_resume_device(json_message, True)
    elif intent == "user_Q52Q01Nyv__ShoppingList":
        tts_say("Sorry, I can't add to your grocery list yet")
    else:
        tts_say("Sorry, I don't understand what you're asking")

def handle_activate_deactivate_object(json_message, activate):
    devices = [device for device in json_message.get('slots') if device['entity'] == "objectType"]
    for device in devices:
        action = "on" if activate else "off"
        tts_say("Turning {} {}".format(action, device['value']['value']))

def handle_pause_resume_device(json_message, pause):
    if pause:
        tts_say("Sorry, I can't pause devices yet")
    else:
        tts_say("Sorry, I can't resume devices yet")

def tts_say(message):
    remote.call_service(api, "script", "snips_voice", {"message": message, "room": room})

if __name__ == '__main__':
    topic = sys.argv[1]
    raw_payload = sys.argv[2]

    json_payload = {}
    try:
        json_payload = json.loads(raw_payload)
        room = topic.split("/")[1]
    except:
        tts_say("Sorry, I'm unable to understand your request")
        sys.exit(1)

    handle_json_request(json_payload)
