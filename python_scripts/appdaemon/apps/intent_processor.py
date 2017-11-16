#!/srv/homeassistant/bin/python3
import json
import os
import random
from util import hassutil
import appdaemon.appapi as appapi
from intent_handlers import power_intent_handler
from intent_handlers import talk_intent_handler

class IntentReceiver(appapi.AppDaemon):
    def __init__(self, name, logger, error, args, global_vars):
        super().__init__(name, logger, error, args, global_vars)
        self.received_room = None
        self.group_yaml = None

    def initialize(self):
        self.group_yaml = hassutil.read_config_file(os.path.join(hassutil.HASS_DIR, hassutil.GROUPS))
        if self.group_yaml:
            self.log("Successfully parsed groups.yaml")
        else:
            self.log("Error parsing groups.yaml")
        self.listen_state(self.on_assistant_command, "sensor.assistant_command_sensor")

    def on_assistant_command(self, entity, attribute, old, new, kwargs):
        json_payload = {}
        try:
            payload = new
            json_payload = json.loads(payload)
        except:
            hassutil.tts_say(self, "Sorry, Im unable to understand your request", tts_room=self.received_room)

        self.handle_json_request(json_payload)

    def handle_json_request(self, json_message):
        self.received_room = json_message.get('source')
        intent = json_message.get('intent_type')
        if intent == power_intent_handler.INTENT:
            power_intent_handler.handle(self, json_message, self.received_room, self.group_yaml)
        elif intent == "MediaIntent":
            hassutil.tts_say(self, "Sorry, I cant control media yet", tts_room=self.received_room)
        elif intent == "LevelIntent":
            hassutil.tts_say(self, "Sorry, I cant control device levels yet", tts_room=self.received_room)
        elif intent == talk_intent_handler.INTENT:
            talk_intent_handler.handle(self, json_message, self.received_room)
        elif intent == "ListIntent":
            hassutil.tts_say(self, "Sorry, I cant manage your lists yet", tts_room=self.received_room)
        elif intent == "SceneIntent":
            hassutil.tts_say(self, "Actually, its fuckin not", tts_room=self.received_room)
        else:
            hassutil.tts_say(self, "Sorry, I dont understand what youre asking", tts_room=self.received_room)
