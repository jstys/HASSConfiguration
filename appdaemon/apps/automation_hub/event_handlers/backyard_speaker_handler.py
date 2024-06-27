import event_dispatcher
from util import logger
from events.media_player_event import MediaPlayerEvent
from actions.switch_action import SwitchAction

def on_filter(event: MediaPlayerEvent):
    return event.prev_state == "off" and event.state != "unavailable" and event.media_player_name == "Backyard Speaker"

def off_filter(event: MediaPlayerEvent):
    return event.state == "off" and event.media_player_name == "Backyard Speaker"

def register_callbacks():
    event_dispatcher.register_callback(on_backyard_speaker_cast, MediaPlayerEvent.__name__, event_filter=on_filter)
    event_dispatcher.register_callback(on_backyard_speaker_stop, MediaPlayerEvent.__name__, event_filter=off_filter)
    
def on_backyard_speaker_cast(event: MediaPlayerEvent):
    logger.info("Started backyard cast")
    SwitchAction().add_switch("Backyard Receiver Outlet").turn_on()

def on_backyard_speaker_stop(event: MediaPlayerEvent):
    logger.info("Stopped backyard cast")
    SwitchAction().add_switch("Backyard Receiver Outlet").turn_off()