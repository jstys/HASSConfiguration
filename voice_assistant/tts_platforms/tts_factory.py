from tts_platforms.picotts import PicoTTS
from tts_platforms.googletts import GoogleTTS

PICO_ENGINE = "pico"
GOOGLE_ENGINE = "google"

def create_tts(tts_platform, tts_config):
    if tts_platform == PICO_ENGINE:
        return create_pico_tts(tts_config)
    elif tts_platform == GOOGLE_ENGINE:
        return create_google_tts(tts_config)
    else:
        return None

def create_pico_tts(tts_config):
    tts = PicoTTS()
    if not tts.validate_config():
        return None
    else:
        return tts
        
def create_google_tts(tts_config):
    tts = GoogleTTS()
    if not tts.validate_config():
        return None
    else:
        return tts
        

