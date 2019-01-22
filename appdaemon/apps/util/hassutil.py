import yaml
import os
import json

import logger

HASS_DIR = "/home/homeassistant/.homeassistant"
APPD_DIR = "/home/homeassistant/appdaemon"
GROUPS = os.path.join(HASS_DIR, "groups", "groups.yaml")
SECRETS = os.path.join(HASS_DIR, "secrets.yaml")
ENTITY_MAP = os.path.join(APPD_DIR, "apps", "util", "entity_map.yaml")
BROADCAST_ROOM = "broadcast"
AFFIRMATIVE_RESPONSES = ["sure thing", "you got it", "as you wish", "no worries", "roger that"]
OBJECT_MAP = {
    "LightObject": ["light", "lights", "hi_hats"],
    "LampObject": ["lamp", "lamps"],
    "ACObject": ["ac", "air_conditioner"],
    "MediaObject": ["tv", "speaker", "speakers", "smartcast"],
    "InputName": ["tv_input"]
}
API_HANDLE = None

class Entity(object):
    def __init__(self, fully_qualified_name):
        fqn_split = fully_qualified_name.split(".")
        self.domain = fqn_split[0].strip()
        self.name = fqn_split[1].strip()
        self.entity_id = fully_qualified_name

    @classmethod
    def fromSplitName(cls, domain, name):
        return cls(".".join([domain, name]))

def set_api_handle(handle):
    global API_HANDLE
    API_HANDLE = handle

def read_config_file(filename):
    try:
        with open(filename) as yamlfile:
            return yaml.load(yamlfile)
    except:
        return {}

def gui_notify(title, message):
    call_service("persistent_notification", "create", title=title, message=message)

def join_notify(target, message, title="Home Assistant"):
    call_service("notify", target, message=message, title=title)

def tts_say(message, tts_room):
    call_service("mqtt", "publish", topic="snips/{}/tts/say".format(tts_room), payload=json.dumps({"text": message, "siteId": tts_room}))

def tts_broadcast(message, source="HASS"):
    call_service("script", "assistant_broadcast", message=message, source=source)
    
def disable_snips_hotword(room):
    call_service("mqtt", "publish", topic="snips/{}/hotword/toggleOff".format(room), payload=json.dumps({"siteId": room}))
    
def enable_snips_hotword(room):
    call_service("mqtt", "publish", topic="snips/{}/hotword/toggleOn".format(room), payload=json.dumps({"siteId": room}))
    
def lock(lock_entity):
    call_service("lock", "lock", entity_id=lock_entity.entity_id)
    
def unlock(lock_entity):
    call_service("lock", "unlock", entity_id=lock_entity.entity_id)

def turn_on(entity, brightness_pct=100, color_temp=255):
    if API_HANDLE is not None:
        if entity.domain == "light":
            API_HANDLE.turn_on(entity.entity_id, brightness_pct=float(brightness_pct), color_temp=color_temp, namespace="hass")
        else:
            API_HANDLE.turn_on(entity.entity_id, namespace="hass")
    else:
        logger.error("API Handle is None")

def toggle(entity):
    if API_HANDLE is not None:
        API_HANDLE.toggle(entity.entity_id, namespace="hass")
    else:
        logger.error("API Handle is None")

def set_light_effect(entity, effect=None):
    if API_HANDLE is not None:
        if effect:
            API_HANDLE.turn_on(entity.entity_id, effect=effect, namespace="hass")
        else:
            logger.error("Missing effect")
    else:
        logger.error("API Handle is None")

def set_light_color(entity, color=None):
    if API_HANDLE:
        if color:
            API_HANDLE.turn_on(entity.entity_id, color_name=color, namespace="hass")
        else:
            logger.error("Missing color")
    else:
        logger.error("API Handle is None")

def turn_off(entity):
    if API_HANDLE:
        API_HANDLE.turn_off(entity.entity_id, namespace="hass")
    else:
        logger.error("API Handle is None")
        
def set_level(entity, brightness_pct):
    if API_HANDLE:
        if entity.domain == "light":
            API_HANDLE.turn_on(entity.entity_id, brightness_pct=float(brightness_pct), namespace="hass")
        else:
            logger.error("Can't set level on non-light entity")
    else:
        logger.error("API Handle is None")

def call_service(domain, action, **kwargs):
    if API_HANDLE:
        API_HANDLE.call_service("/".join([domain, action]), namespace="hass", **kwargs)
    else:
        logger.error("API Handle is None")

def fire_event(event, **kwargs):
    if API_HANDLE:
        API_HANDLE.fire_event(event, namespace="hass", **kwargs)
    else:
        logger.error("API Handle is None")

def is_someone_home():
    if API_HANDLE:
        return API_HANDLE.anyone_home()
    else:
        logger.error("API Handle is None")