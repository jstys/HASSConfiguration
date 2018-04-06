import subprocess

from tts_platforms.itts import ITTS
from gtts import gTTS

class GoogleTTS(ITTS):
    def __init__(self, config):
        super().__init__(config)
        
    def validate_config(self):
        return True
        
    def speak(self, message):
        tts = gTTS(text=message, lang='en', slow=False)
        tts.save("./audio/tmp.mp3")
        subprocess.call(['mpg123', './audio/tmp.mp3'])