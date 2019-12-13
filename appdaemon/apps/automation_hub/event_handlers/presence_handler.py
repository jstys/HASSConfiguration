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
    if event.new == "not_home":
        on_person_away(event.name)
    elif event.new == "home":
        on_person_home(event.name)

def on_person_away(name):
    logger.info("{} has left home".format(name))
    
    if not hassutil.is_someone_home():
        handle_nobody_home()
    
    if name == "jim_presence":
        PushNotifyAction().add_target("jim_cell").set_message("Come back soon!").notify()


def on_person_home(name):
    logger.info("{} has arrived home".format(name))
    
    handle_somebody_home()

    if not state_machine.is_sun_up():
        LightAction().add_light("driveway_light").turn_on()
    
    if name == "jim_presence":
        PushNotifyAction().add_target("jim_cell").set_message("Welcome home!").notify()
        
        
def handle_nobody_home():
    logger.info("Nobody home...")

    if not state_machine.is_guest_state_enabled():
        all_tvs = entity_map.find_type_entities("tv")
        
        LightAction().add_light("manual_off_lights").turn_off()
        MediaPlayerAction().add_media_players(all_tvs).turn_off()
        DoorLockAction().add_lock("front_entrance_lock").lock()
        
        # Turn off sleep mode
        hassutil.turn_off(hassutil.Entity(entity_map.name_map["sleep_mode"]))
        
        #TODO: schedule timer for simulating someone being home
    
def handle_somebody_home():
    logger.info("Someone is home now...")
    
    LightAction().add_lights(["kitchen_lights", "dining_room_light", "living_room_lamps"]).turn_on()
    
    #TODO: cancel timer for simulating someone being home
    #TODO: set lights / thermostats / tvs