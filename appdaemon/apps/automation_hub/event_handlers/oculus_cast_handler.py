import time
import event_dispatcher
from util import logger
from util import entity_map
from events.media_player_event import MediaPlayerEvent
from actions.media_player_action import MediaPlayerAction

def event_filter(event: MediaPlayerEvent):
    return event.app_name == "Oculus" and event.state == "playing"

def register_callbacks():
    event_dispatcher.register_callback(on_oculus_cast, MediaPlayerEvent.__name__, event_filter=event_filter)
    
def on_oculus_cast(event: MediaPlayerEvent):
    logger.info(f"Oculus cast detected on {event.media_player_name}")

    if event.media_player_name in entity_map.find_type_entities("tv"):
        time.sleep(3)
        MediaPlayerAction().add_media_player(event.media_player_name).mute()
    