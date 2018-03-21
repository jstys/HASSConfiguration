import yaml
import os
import sys

CONFIGURATION_FILE = os.path.join(os.path.realpath(__file__), "voice_assistant.yaml")


class VoiceAssistant():
    
    def __init__(self):
        self._configuration = None
        self._common_config = None
        self._assistant_type = None
        self._assistant_config = None
        self._connection_protocol = None
        self._connection_config = None
        self._assistant = None
        self._connection = None
        
    def start(self):
        if not self.read_configuration():
            sys.exit(1)
            
        if not self.validate_common_config():
            sys.exit(1)
        
        self._connection = self._connection_factory.create_connection(self._connection_protocol, self._connection_config)
        if not self._connection:
            sys.exit(1)
            
        self._assistant = self._assistant_factory.create_assistant(self._assistant_type, self._assistant_config)
        if not self._assistant:
            sys.exit(1)
            
        self._connection.run_in_background()
        self._assistant.run_in_foreground()
        
    def validate_common_config(self):
        pass
    
    def read_configuration(self):
        try:
            self._configuration = yaml.load(CONFIGURATION_FILE)
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
            self._assistant_config = self._configuration[self._assistant_type]
        except:
            print("Invalid configuration of 'assistant_type' in voice_assistant.yaml")
            return False
            
        try:
            self.connection_protocol = self._common_config['connection_protocol']
            self.connection_config = self._configuration[self._connection_protocol]
        except:
            print("Invalid configuration of 'connection_protocol' in voice_assistant.yaml")
            return False
            
    def on_tts_message(self, message):
        pass
    
    def on_broadcast_message(self, message):
        pass
    
    def on_ask_message(self, message):
        pass
    
    def on_broadcast_ask_message(self, message):
        pass

def main():
    assistant = VoiceAssistant()
    assistant.start()
        
    
    

if __name__ == '__main__':
    main()
