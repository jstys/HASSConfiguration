import os
import json
import subprocess

import google.oauth2.credentials
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

import iassistant.IAssistant as IAssistant
import intent_builders.raw_speech_intent_builder as intent_builder

class GoogleAssitant(IAssistant):

    CREDENTIALS_FILE = "credentials.json"

    def __init__(self, config, hotword_detected, intent_built):
        super().__init__(config, hotword_detected, intent_built)
        self._credentials = None
        self._device_model = None

    def validate_config(self):
        try:
            with open(GoogleAssitant.CREDENTIALS_FILE, 'r') as f:
                self._credentials = google.oauth2.credentials.Credentials(token=None, **json.load(f))
        except:
            print("Unable to load GoogleAssistant credentials file (credentials.json)")
            return False

        try:
            self._device_model = self._config['device_model']
        except:
            print("device_model not configured in GoogleAssistant configuration")
            return False

        return True

    def run_in_foreground(self):
        with Assistant(self._credentials, self._device_model) as assistant:
            for event in assistant.start():
                self.process_event(event, assistant)

    def process_event(self, event, assistant):
        if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            subprocess.call(['aplay', 'hotword.wav'])
            self._on_hotword_detected()

        if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
            subprocess.call(['aplay', 'finished.wav'])
            
            text = event.args.get('text')
            print("Raw: {}".format(text))

            intent, massaged_text = intent_builder.parse_intent(text)
            if intent is not None:
                assistant.stop_conversation()
                intent['raw'] = massaged_text
                self._on_intent_built(intent)
