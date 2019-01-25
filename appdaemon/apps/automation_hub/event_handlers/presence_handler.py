from automation_hub import event_dispatcher
from automation_hub import state_machine
from util import logger
from util import hassutil
from util import entity_map
from events.presence_event import PresenceEvent
from actions.push_notify_action import PushNotifyAction
from actions.light_action import LightAction
from actions.media_player_action import MediaPlayerAction
from actions.door_lock_action import DoorLockAction

def register_callbacks():
    event_dispatcher.register_callback(on_presence_changed, PresenceEvent.__name__)
    
def on_presence_changed(event):
    if event.old == "home" and event.new == "not_home":
        on_person_away(event.name)
    elif event.old == "not_home" and event.new == "home":
        on_person_home(event.name)

def on_person_away(name):
    logger.info("{} has left home".format(name))
    
    if not hassutil.is_someone_home():
        handle_nobody_home()
    
    if name == "jim_presence":
        PushNotifyAction().add_target("jim_cell_notify").set_message("Come back soon!").notify()


def on_person_home(name):
    logger.info("{} has arrived home".format(name))
    
    if state_machine.get_state(state_machine.NOBODY_HOME_STATE):
        handle_somebody_home()
    
    if name == "jim_presence":
        PushNotifyAction().add_target("jim_cell_notify").set_message("Welcome home!").notify()
        
        
def handle_nobody_home():
    logger.info("Nobody home...")
    state_machine.set_state(state_machine.NOBODY_HOME_STATE, True)
    
    all_lights = entity_map.find_type_entities("light")
    all_tvs = entity_map.find_type_entities("tv")
    
    LightAction().add_lights(all_lights).turn_off()
    MediaPlayerAction().add_media_players(all_tvs).turn_off()
    DoorLockAction().add_lock("front_door_lock").lock()
    
    # Turn off sleep mode
    hassutil.turn_off(hassutil.Entity(entity_map.name_map["sleep_mode"]))
    
    #TODO: schedule timer for simulating someone being home
    
def handle_somebody_home():
    logger.info("Someone is home now...")
    state_machine.set_state(state_machine.NOBODY_HOME_STATE, False)
    
    #TODO: cancel timer for simulating someone being home
    #TODO: set lights / thermostats / tvs