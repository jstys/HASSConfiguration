from util.entity_map import assistant_list
from util import hassutil
from util import logger

class AssistantAction():
    def __init__(self):
        self._assistants = []

    def add_assistants(self, assistants):
        for assistant in assistants:
            self.add_assistant(assistant)

        return self

    def add_assistant(self, assistant):
        if assistant in assistant_list:
            self._assistants.append(assistant)
        else:
            logger.error("Unable to add unknown assistant to AssistantAction: {}".format(assistant))

        return self

    def tts_say(self, message):
        for assistant in self._assistants:
            hassutil.tts_say(message, assistant)
    
    def broadcast(self, message):
        for assistant in assistant_list:
            hassutil.tts_say(message, assistant)
    
    def enable_hotword(self):
        for assistant in self._assistants:
            hassutil.enable_snips_hotword(assistant)
    
    def disable_hotword(self):
        for assistant in self._assistants:
            hassutil.disable_snips_hotword(assistant)
    