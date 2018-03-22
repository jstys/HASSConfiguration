import os
import sys
import subprocess
import datetime
import json

import yaml
import assistants.assistant_factory as assistant_factory
import connections.connection_factory as connection_factory

class VoiceAssistant():

    CONFIGURATION_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "voice_assistant.yaml")
    
    def __init__(self):
        self._configuration = None
        self._common_config = None
        self._assistant_type = None
        self._assistant_config = None
        self._connection_protocol = None
        self._connection_config = None
        self._assistant = None
        self._connection = None
        self._room_name = None
        
    def start(self):
        if not self.read_configuration():
            sys.exit(1)
            
        if not self.validate_common_config():
            sys.exit(1)
        
        self._connection = connection_factory.create_connection(self._connection_protocol, 
                                                                self._connection_config,
                                                                self.on_tts_message,
                                                                self.on_broadcast_message,
                                                                self.on_ask_message,
                                                                self.on_broadcast_ask_message)
        if not self._connection:
            sys.exit(1)
            
        self._assistant = assistant_factory.create_assistant(self._assistant_type, 
                                                             self._assistant_config,
                                                             self.on_hotword_detected,
                                                             self.on_intent_built)
        if not self._assistant:
            sys.exit(1)
            
        self._connection.run_in_background()
        self._assistant.run_in_foreground()
        
    def validate_common_config(self):
        try:
            self._room_name = self._common_config['room_name']
        except:
            print("Missing room_name in commmon configuration")
            return False

        return True
    
    def read_configuration(self):
        try:
            with open(VoiceAssistant.CONFIGURATION_FILE, 'r') as config_file:
                self._configuration = yaml.load(config_file)
        except:
            print("Unable to load configuration file (voice_assistant.yaml) for voice_assistant... Exiting...")
            return False
        
        try:
            self._common_config = self._configuration['common']
        except:
            print("Missing required 'common' section of voice_assistant.yaml")
            return False
            
        try:
            self._assistant_type = self._common_config['assistant_type']
            self._assistant_config = self._configuration['assistant'][self._assistant_type]
        except:
            print("Invalid configuration of 'assistant_type' in voice_assistant.yaml")
            return False
            
        try:
            self._connection_protocol = self._common_config['connection_protocol']
            self._connection_config = self._configuration['connection'][self._connection_protocol]
        except:
            print("Invalid configuration of 'connection_protocol' in voice_assistant.yaml")
            return False
            
    def on_tts_message(self, message):
        self._speak_message(message)
    
    def on_broadcast_message(self, message, source):
        if source == self._room_name:
            message = "Your message has been shared"

        self._speak_message(message)

    def _speak_message(self, message):
        pico_command = ['pico2wave', '-l', 'en-US', '-w', 'tmp.wav', message]
        subprocess.call(pico_command)
        subprocess.call(['aplay', 'tmp.wav'])
    
    def on_ask_message(self, message, followed_intent=None):
        self._speak_message(message)
        self._assistant.recognize_speech(followed_intent)
    
    def on_broadcast_ask_message(self, message, source):
        if source == self._room_name:
            message = "Your question has been asked"

        self._speak_message(message)

    def on_hotword_detected(self):
        pass

    def on_intent_built(self, intent):
        intent['source'] = self._room_name
        intent['timestamp'] = str(datetime.datetime.now())
        self._connection.send_message(json.dumps(intent), source=self._room_name)

def main():
    assistant = VoiceAssistant()
    assistant.start()
        
if __name__ == '__main__':
    main()
