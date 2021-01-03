import json
import functools

import event_dispatcher
import state_machine
import timer_manager
from util import logutil
from util import hassutil
from util.entity_map import room_map
from util.entity_map import find_room_entities
from util.entity_map import assistant_list
from actions.light_action import LightAction
from actions.media_player_action import MediaPlayerAction
from actions.assistant_action import AssistantAction
from actions.vacuum_action import VacuumAction
from actions.join_action import JoinAction
from events.mqtt_event import MQTTEvent

logger = logutil.get_logger("automation_hub")

def event_filter(event):
    return "snips/intent/" in event.topic or event.topic == "snips/nluIntent"

def register_callbacks():
    event_dispatcher.register_callback(on_intent, MQTTEvent.__name__, event_filter=event_filter)
    
def on_intent(event):
    parsed = {}
    try:
        parsed = json.loads(event.payload)
    except:
        pass
    
    source = parsed.get("siteId")
    raw = parsed.get("input")
    intent = parsed.get("intent")
    slotMap = {}
    slots = parsed.get("slots")

    if slots:
        for slot in slots:
            slotName = slot.get("slotName")
            slotValue = slot.get("value")
            
            if slotName == "room":
                slotValue["value"] = slotValue["value"].replace(" ", "_")
                
            slotMap[slotName] = slotValue
            
    if intent and source and raw:
        logger.info("Received Snips intent from {} with raw input ({})".format(source, raw))
        name = intent.get("intentName").split(":")
        name = name[len(name)-1]
        if name == "thermostatSet":
            handle_thermostat(intent, source, raw, slotMap)
        elif name == "thermostatShift":
            pass
        elif name == "thermostatTurnOff":
            pass
        elif name == "tvOn":
            handle_tv_on(intent, source, raw, slotMap)
        elif name == "tvOff":
            handle_tv_off(intent, source, raw, slotMap)
        elif name == "tvInput":
            handle_tv_input(intent, source, raw, slotMap)
        elif name == "lightOn":
            handle_light_on(intent, source, raw, slotMap)
        elif name == "lightOff":
            handle_light_off(intent, source, raw, slotMap)
        elif name == "lightDim":
            handle_light_dim(intent, source, raw, slotMap)
        elif name == "lightBrighten":
            handle_light_brighten(intent, source, raw, slotMap)
        elif name == "setScene":
            handle_set_scene(intent, source, raw, slotMap)
        elif name == "SetTimer":
            handle_set_timer(intent, source, raw, slotMap)
        elif name == "StopTimer":
            handle_stop_timer(intent, source, raw, slotMap)
        elif name == "vacuumStart":
            handle_start_vacuum(intent, source, raw, slotMap)
        elif name == "vacuumStop":
            handle_stop_vacuum(intent, source, raw, slotMap)
        elif name == "vacuumLocate":
            handle_locate_vacuum(intent, source, raw, slotMap)
        elif name == "findPhone":
            handle_find_phone(intent, source, raw, slotMap)
        elif name == "openGarage":
            handle_open_garage(intent, source, raw, slotMap)
        elif name == "closeGarage":
            handle_close_garage(intent, source, raw, slotMap)
    else:
        logger.error("Missing valid snips intent")

def handle_thermostat(intent, source, raw, slotMap):
    logger.info("Received Thermostat set intent from snips")

def handle_tv_on(intent, source, raw, slotMap):
    logger.info("Received TV On intent from snips")
    
    room = slotMap["room"]["value"] if "room" in slotMap else source

    if room in room_map:
        media_players = find_room_entities("tv", room)
        media_players.extend(find_room_entities("speakers", room))
        MediaPlayerAction().add_media_players(media_players).turn_on()
        

def handle_tv_off(intent, source, raw, slotMap):
    logger.info("Received TV Off intent from snips")
    
    room = slotMap["room"]["value"] if "room" in slotMap else source

    if room in room_map:
        media_players = find_room_entities("tv", room)
        media_players.extend(find_room_entities("speakers", room))
        MediaPlayerAction().add_media_players(media_players).turn_off()
        
def handle_tv_input(intent, source, raw, slotMap):
    logger.info("Received TV Input intent from snips")
    
    tv_input = slotMap["inputName"]["value"]
    
    media_players = find_room_entities("tv", source)
    MediaPlayerAction().add_media_players(media_players).change_input(tv_input)

def handle_light_on(intent, source, raw, slotMap):
    logger.info("Received Light On intent from snips")
    
    room = slotMap["room"]["value"] if "room" in slotMap else source

    if room in room_map:
        lights = find_room_entities("light", room)
        LightAction().add_lights(lights).turn_on()

def handle_light_off(intent, source, raw, slotMap):
    logger.info("Received Light off intent from snips")

    room = slotMap["room"]["value"] if "room" in slotMap else source

    if room in room_map:
        lights = find_room_entities("light", room)
        LightAction().add_lights(lights).turn_off()
        
def handle_light_dim(intent, source, raw, slotMap):
    pass

def handle_light_brighten(intent, source, raw, slotMap):
    pass

def handle_set_scene(intent, source, raw, slotMap):
    pass
        
def handle_set_timer(intent, source, raw, slotMap):
    if not "timer_name" in slotMap or not "timer_duration" in slotMap:
        logger.error("Must have name and duration of timer")
        return
    
    if source not in assistant_list:
        logger.error("Invalid source room supplied")
        return
    
    duration = slotMap["timer_duration"]
    name = slotMap["timer_name"]["value"]
    action = AssistantAction().add_assistant(source).tts_say
    callback = functools.partial(action, "{} timer has finished".format(name))
    timer_manager.start_timer(name, callback, seconds=duration["seconds"], minutes=duration["minutes"], hours=duration["hours"], days=duration["days"])
    
    AssistantAction().add_assistant(source).tts_say("{} timer started".format(name))

def handle_stop_timer(intent, source, raw, slotMap):
    if not "timer_name" in slotMap:
        logger.error("Must have name of timer")
        return
    
    if source not in assistant_list:
        logger.error("Invalid source room supplied")
        return
    
    name = slotMap["timer_name"]["value"]
    timer_manager.cancel_timer(name)
    AssistantAction().add_assistant(source).tts_say("{} timer cancelled".format(name))

def handle_start_vacuum(intent, source, raw, slotMap):
    logger.info("Starting the vacuum")
    VacuumAction().add_vacuum("robot_vacuum").start()

def handle_stop_vacuum(intent, source, raw, slotMap):
    logger.info("Stopping the vacuum")
    VacuumAction().add_vacuum("robot_vacuum").return_home()

def handle_locate_vacuum(intent, source, raw, slotMap):
    logger.info("Locating the vacuum")
    VacuumAction().add_vacuum("robot_vacuum").locate()
    
def handle_find_phone(intent, source, raw, slotMap):
    logger.info("Handling find phone query")
    owner = slotMap["owner"]["value"]
    JoinAction().add_target("{}_cell".format(owner)).ring()

def handle_open_garage(intent, source, raw, slotMap):
    pass

def handle_close_garage(intent, source, raw, slotMap):
    pass