#!/srv/homeassistant/bin/python3
import json
import os
import importlib
import re
from util import hassutil
import appdaemon.appapi as appapi

class IntentReceiver(appapi.AppDaemon):
    def __init__(self, name, logger, error, args, global_vars):
        super().__init__(name, logger, error, args, global_vars)
        self.received_room = None
        self.group_yaml = None
        self.handler_map = {}
        self._load_handlers()

    def _load_handlers(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        handler_path = os.path.join(cwd, "intent_handlers")
        ls_output = os.listdir(handler_path)
        module_files = [pyfile for pyfile in ls_output if re.match(r'^.+\.py$', pyfile) and '__init__.py' not in pyfile]
        for module_name in module_files:
            module = importlib.import_module(".".join(["intent_handlers", module_name.replace('.py', '')]))
            self.handler_map[module.INTENT] = module

    def initialize(self):
        self.group_yaml = hassutil.read_config_file(hassutil.GROUPS)
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
        except ValueError:
            hassutil.tts_say(self, "Sorry, Im unable to understand your request", tts_room=self.received_room)

        self.handle_json_request(json_payload)

    def handle_json_request(self, json_message):
        self.received_room = json_message.get('source')
        intent = json_message.get('intent_type')
        target_handler = self.handler_map.get(intent)
        if target_handler is not None:
            target_handler.handle(self, json_message, self.received_room, self.group_yaml)
        else:
            hassutil.tts_say(self, "Sorry, I dont understand what youre asking", tts_room=self.received_room)