import event_dispatcher
from util import logutil
import timer_manager
from events.input_event import InputEvent
from actions.media_player_action import MediaPlayerAction

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return event.name == "master_bedroom_whitenoise"

def register_callbacks():
    event_dispatcher.register_callback(on_state_changed, InputEvent.__name__, event_filter=event_filter)
    
def on_state_changed(event):
    if event.new == "off":
        on_disabled(event)
    elif event.new == "on":
        on_enabled(event)
    else:
        logger.warning("Invalid state transition for privacy mode")

def on_disabled(event):
    timer_manager.cancel_timer("white_noise_restart")
    media_action = MediaPlayerAction().add_media_player("master_bedroom_mpd")
    media_action.stop()
    media_action.clear_playlist()

def on_enabled(event):
    play_white_noise()

def play_white_noise():
    mp_action = MediaPlayerAction().add_media_player("master_bedroom_mpd")
    mp_action.set_volume(0.8)
    mp_action.play_music("http://10.0.0.6:8123/local/white_noise.mp3")
    timer_manager.start_timer("white_noise_restart", play_white_noise, hours=1)
