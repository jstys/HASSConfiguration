from automation_hub import event_dispatcher
from automation_hub import timer_manager
from util import entity_map
from util import logger
from util import hassutil
from events.input_event import InputEvent
from actions.door_lock_action import DoorLockAction
from actions.vacuum_action import VacuumAction
from actions.light_action import LightAction
from actions.assistant_action import AssistantAction
from actions.join_action import JoinAction
from actions.media_player_action import MediaPlayerAction

def event_filter(event):
    return event.name == "sleep_mode"

def register_callbacks():
    event_dispatcher.register_callback(on_state_changed, InputEvent.__name__, event_filter=event_filter)
    
def on_state_changed(event):
    if event.new == "off":
        on_sleep_state_disabled(event)
    elif event.new == "on":
        on_sleep_state_enabled(event)
    else:
        logger.warning("Invalid state transition for sleep state")

def on_sleep_state_enabled(event):
    logger.info("Sleep state enabled")
    
    DoorLockAction().add_lock("front_entrance_lock").lock()
    LightAction().add_lights(["manual_off_lights", "hallway_lights"]).turn_off()
    assistant_action = AssistantAction().add_assistant("master_bedroom")
    assistant_action.disable_hotword()
    assistant_action.disable_led()
    JoinAction().add_target("jim_cell").send_taker_command("bed_command")
    MediaPlayerAction().add_media_player("master_bedroom_mpd").set_volume(0.8)
    MediaPlayerAction().add_media_player("living_room_tv").turn_off()
    play_white_noise()

def play_white_noise():
    MediaPlayerAction().add_media_player("master_bedroom_mpd").play_music("http://10.0.0.6:8123/local/white_noise.mp3")
    timer_manager.start_timer("white_noise_restart", play_white_noise, hours=1)

def on_sleep_state_disabled(event):
    logger.info("Sleep state disabled")

    assistant_action = AssistantAction().add_assistant("master_bedroom")
    assistant_action.enable_hotword()
    assistant_action.enable_led()
    JoinAction().add_target("jim_cell").send_taker_command("awake_command")
    timer_manager.cancel_timer("white_noise_restart")
    media_action = MediaPlayerAction().add_media_player("master_bedroom_mpd")
    media_action.stop()
    media_action.clear_playlist()