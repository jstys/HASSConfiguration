import subprocess

from tts_platforms.itts import ITTS

class PicoTTS(ITTS):
    def __init__(self, config):
        super().__init__(config)
        
    def validate_config(self):
        return True
        
    def speak(self, message):
        pico_command = ['pico2wave', '-l', 'en-US', '-w', './audio/tmp.wav', message]
        subprocess.call(pico_command)
        subprocess.call(['aplay', './audio/tmp.wav'])