#!/srv/homeassistant/bin/python3
import json
import sys
import random
import hassutil
import appdaemon.appapi as appapi

BROADCAST_ROOM = "broadcast"
AFFIRMATIVE_RESPONSES = ["sure thing", "you got it", "as you wish", "no worries", "roger that"]

class IntentReceiver(appapi.AppDaemon):
    def __init__(self):
        self.received_room = None

    def initialize(self):
        self.listen_event(self.on_assistant_command, "assistant_command")

    def on_assistant_command(self, topic, payload):
        json_payload = {}
        try:
            json_payload = json.loads(payload)
            self.received_room = topic.split("/")[1]
        except:
            self.tts_say("Sorry, Im unable to understand your request")

        self.handle_json_request(json_payload)

    def handle_json_request(self, json_message):
        intent = json_message['intent_type']
        if intent == "PowerIntent":
            self.handle_power_intent(json_message)
        elif intent == "MediaIntent":
            self.tts_say("Sorry, I cant control media yet")
        elif intent == "LevelIntent":
            self.tts_say("Sorry, I cant control device levels yet")
        elif intent == "BroadcastIntent" or intent == "TalkIntent":
            self.tts_say("Sorry, I cant broadcast messages yet")
        elif intent == "ListIntent":
            self.tts_say("Sorry, I cant manage your lists yet")
        elif intent == "SceneIntent":
            self.tts_say("Actually, its fuckin not")
        else:
            self.tts_say("Sorry, I dont understand what youre asking")

    def handle_power_intent(self, json_message):
        room = json_message.get('Room')
        room = self.received_room if room is None else room

        is_on_action = (json_message['PowerVerb'] == "turn on")

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
            devices = [entity for entity in hassutil.get_tv_input_scripts(room)]
        elif room == "house":
            devices = [entity for entity in hassutil.get_all_switches_and_lights()]
        else:
            devices = [entity for entity in hassutil.get_group_switches_and_lights(room)]

        level = json_message.get('Percentage')
        allMod = json_message.get('AllModifier') is not None

        if allMod:
            if deviceType == "LightObject":
                self.tts_say(random.choice(AFFIRMATIVE_RESPONSES))
                for entity in devices:
                    if "lamp" in entity.name or "light" in entity.name:
                        self.turn_off_on(entity, is_on_action, level)
        else:
            self.tts_say(random.choice(AFFIRMATIVE_RESPONSES))
            for entity in devices:
                if device in entity.name:
                    self.turn_off_on(entity, is_on_action, level)

    def turn_off_on(self, entity, on, brightness):
        brightness = 75 if brightness is None else brightness.replace("%", "")
        if on:
            if entity.domain == "light":
                self.call_service(".".join([entity.domain, "turn_on"]), {"entity_id": entity.entity_id, "brightness_pct": brightness})
            else:
                self.call_service(".".join([entity.domain, "turn_on"]), {"entity_id": entity.entity_id})
        else:
            self.call_service(".".join([entity.domain, "turn_off"]), {"entity_id": entity.entity_id})

    def log(self, message):
        self.call_service(".".join(["logbook", "log"]), {"name": "intent_processor.py", "message": message})

    def tts_say(self, message, tts_room=None):
        tts_room = self.received_room if tts_room is None else tts_room
        if tts_room == BROADCAST_ROOM:
            self.call_service(".".join(["script", "assistant_broadcast"]), {"message": message, "source": self.received_room})
        else:
            self.call_service(".".join(["script", "assistant_voice"]), {"message": message, "room": tts_room})
