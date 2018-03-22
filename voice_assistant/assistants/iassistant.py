class IAssistant():
    def __init__(self, config, hotword_detected, intent_built):
        self._config = config
        self._on_hotword_detected = hotword_detected
        self._on_intent_built = intent_built

    def validate_config(self):
        pass

    def run_in_foreground(self):
        pass

    def recognize_speech(self, followed_intent=None):
        pass