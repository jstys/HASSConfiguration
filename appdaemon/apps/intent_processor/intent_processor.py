#!/srv/homeassistant/bin/python3
import json
import os
import importlib
import re
import hassutil
import appdaemon.plugins.hass.hassapi as hass

class IntentReceiver(hass.Hass):
    def __init__(self, ad, name, logger, error, args, config, app_config, global_vars):
        super().__init__(ad, name, logger, error, args, config, app_config, global_vars)
        self.received_room = None
        self.group_yaml = None
        self.handler_map = {}
        self.handler_events = {}
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
        self.handler_events.clear()
        self.group_yaml = hassutil.read_config_file(hassutil.GROUPS)
        if self.group_yaml:
            self.log("Successfully parsed groups.yaml")
        else:
            self.log("Error parsing groups.yaml")
        self.listen_event(self.on_assistant_command, "VOICE_ASSISTANT_INTENT")
        for _, handler in self.handler_map.items():
            handler.initialize(self)

    def register_handler_event(self, callback, event):
        if event not in self.handler_events:
            self.handler_events[event] = []
            self.listen_event(self.on_handler_event, event)

        self.handler_events[event].append(callback)

    def on_handler_event(self, event, data, kwargs):
        callbacks = self.handler_events.get(event)
        if callbacks:
            for callback in callbacks:
                callback(self, event, data, kwargs)


    def on_assistant_command(self, event_name, data, kwargs):
        json_payload = {}
        try:
            payload = data.get('payload')
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
