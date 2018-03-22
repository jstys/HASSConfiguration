class IConnection():
    def __init__(self, config, on_tts, on_broadcast, on_ask, on_broadcast_ask):
        self._config = config
        self._on_tts_message = on_tts
        self._on_broadcast_message = on_broadcast
        self._on_ask_message = on_ask
        self._on_broadcast_ask_message = on_broadcast_ask
    
    def validate_config(self):
        pass
    
    def run_in_background(self):
        pass

    def send_message(self, message, source=None):
        pass