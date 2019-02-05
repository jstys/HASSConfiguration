from util.entity_map import assistant_list
from util import hassutil
from util import logger

class TTSAction():
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
            logger.error("Unable to add unknown assistant to TTSAction: {}".format(assistant))

        return self

    def say(self, message):
        for assistant in self._assistants:
            hassutil.tts_say(message, assistant)
            
    def broadcast(self, message):
        for assistant in assistant_list:
            hassutil.tts_say(message, assistant)