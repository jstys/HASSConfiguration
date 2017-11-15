#!/srv/homeassistant/bin/python3
import json
import os
import random
from util import hassutil
import appdaemon.appapi as appapi

BROADCAST_ROOM = "broadcast"
AFFIRMATIVE_RESPONSES = ["sure thing", "you got it", "as you wish", "no worries", "roger that"]

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
            self.tts_say("Sorry, Im unable to understand your request")

        self.handle_json_request(json_payload)

    def handle_json_request(self, json_message):
        self.received_room = json_message.get('source')
        intent = json_message.get('intent_type')
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

        is_on_action = (json_message.get('PowerVerb') == "turn on")

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
            devices = [entity for entity in hassutil.get_tv_input_scripts(room, self.group_yaml)]
        elif room == "house":
            devices = [entity for entity in hassutil.get_all_switches_and_lights(self.group_yaml)]
        else:
            devices = [entity for entity in hassutil.get_group_switches_and_lights(room, self.group_yaml)]

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
                self.turn_on(entity.entity_id, brightness_pct=brightness)
            else:
                self.turn_on(entity.entity_id)
        else:
            self.turn_off(entity.entity_id)

    def tts_say(self, message, tts_room=None):
        tts_room = self.received_room if tts_room is None else tts_room
        if tts_room == BROADCAST_ROOM:
            self.call_service("/".join(["script", "assistant_broadcast"]), message=message, source=self.received_room)
        else:
            self.call_service("/".join(["script", "assistant_voice"]), message=message, room=tts_room)
