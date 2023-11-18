import event_dispatcher
from util import logger
from events.zwave_scene_event import ZwaveSceneEvent
from actions.light_action import LightAction
from actions.media_player_action import MediaPlayerAction

def event_filter(event):
    return event.name in ["Scene Controller"]

def register_callbacks():
    event_dispatcher.register_callback(on_scene_activated, ZwaveSceneEvent.__name__, event_filter=event_filter)

def on_scene_activated(event: ZwaveSceneEvent):
    if event.scene_id == 1:
        scene_one(event.scene_data)
    elif event.scene_id == 2:
        scene_two(event.scene_data)
    elif event.scene_id == 3:
        scene_three(event.scene_data)
    elif event.scene_id == 4:
        scene_four(event.scene_data)
    elif event.scene_id == 5:
        scene_five(event.scene_data)
    elif event.scene_id == 6:
        scene_six(event.scene_data)
    elif event.scene_id == 7:
        scene_seven(event.scene_data)
    elif event.scene_id == 8:
        scene_eight(event.scene_data)

def scene_one(action):
    if action == "KeyPressed":
        MediaPlayerAction().add_media_player("Living Room TV").toggle_power()

def scene_two(action):
    if action == "KeyPressed":
        MediaPlayerAction().add_media_player("Living Room TV").change_input("tv")

def scene_three(action):
    if action == "KeyPressed" or action == "KeyHeldDown":
        MediaPlayerAction().add_media_player("Living Room TV").volume_up()

def scene_four(action):
    if action == "KeyPressed":
        LightAction().add_light("Living Room Lamps").toggle()

def scene_five(action):
    if action == "KeyPressed":
        MediaPlayerAction().add_media_player("Living Room TV").mute()

def scene_six(action):
    if action == "KeyPressed":
        MediaPlayerAction().add_media_player("Living Room TV").change_input("gaming")

def scene_seven(action):
    if action == "KeyPressed" or action == "KeyHeldDown":
        MediaPlayerAction().add_media_player("Living Room TV").volume_down()

def scene_eight(action):
    if action == "KeyPressed":
        LightAction().add_light("Dining Room Light").toggle()