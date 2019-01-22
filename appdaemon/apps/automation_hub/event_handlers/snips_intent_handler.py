import json
import functools

from automation_hub import event_dispatcher
from automation_hub import state_machine
from automation_hub import timer_manager
from util import logger
from util import hassutil
from util.entity_map import room_map
from util.entity_map import find_room_entities
from actions.light_action import LightAction
from actions.media_player_action import MediaPlayerAction
from events.mqtt_event import MQTTEvent

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
            slotMap[slot.get("slotName")] = slot.get("value")
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
        elif name == "SetTimer":
            handle_set_timer(intent, source, raw, slotMap)
        elif name == "StopTimer":
            handle_stop_timer(intent, source, raw, slotMap)
        elif name == "VacuumStart":
            pass
        elif name == "VacuumStop":
            pass
    else:
        logger.error("Missing valid snips intent")

def handle_thermostat(intent, source, raw, slotMap):
    logger.info("Received Thermostat set intent from snips")

def handle_tv_on(intent, source, raw, slotMap):
    logger.info("Received TV On intent from snips")
    
    room = slotMap["room"]["value"] if "room" in slotMap else source

    if room in room_map:
        media_players = find_room_entities("tv", room).extend(find_room_entities("speakers", room))
        MediaPlayerAction().add_media_players(media_players).turn_on()
        

def handle_tv_off(intent, source, raw, slotMap):
    logger.info("Received TV Off intent from snips")
    
    room = slotMap["room"]["value"] if "room" in slotMap else source

    if room in room_map:
        media_players = find_room_entities("tv", room).extend(find_room_entities("speakers", room))
        MediaPlayerAction().add_media_players(media_players).turn_off()
        
def handle_tv_input(intent, source, raw, slotMap):
    logger.info("Received TV Input intent from snips")

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
        
def handle_set_timer(intent, source, raw, slotMap):
    if not "timer_name" in slotMap or not "timer_duration" in slotMap:
        logger.error("Must have name and duration of timer")
        return
    
    if source not in room_map:
        logger.error("Invalid source room supplied")
        return
    
    duration = slotMap["timer_duration"]
    name = slotMap["timer_name"]
    callback = functools.partial(hassutil.tts_say, "{} timer has finished".format(name), source)
    timer_manager.start_timer(name, callback, seconds=duration["seconds"], minutes=duration["minutes"], hours=duration["hours"], days=duration["days"])
    
    hassutil.tts_say("{} timer started".format(name), source.replace("_", " "))

def handle_stop_timer(intent, source, raw, slotMap):
    if not "timer_name" in slotMap:
        logger.error("Must have name of timer")
        return
    
    if source not in room_map:
        logger.error("Invalid source room supplied")
        return
    
    name = slotMap["timer_name"]
    timer_manager.cancel_timer(name)
    hassutil.tts_say("{} timer cancelled".format(name), source)

    