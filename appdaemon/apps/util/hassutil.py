import yaml
import os
import json

import logutil

APPD_DIR = "/conf"
SECRETS = os.path.join(APPD_DIR, "secrets.yaml")
ENTITY_MAP = os.path.join(APPD_DIR, "apps", "util", "entity_map.yaml")
API_HANDLE = None

logger = logutil.get_logger("automation_hub")

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
            return yaml.safe_load(yamlfile)
    except:
        return {}

def read_binary_file(filename):
    with open(filename, "rb") as binary_file:
        return binary_file.read()

def gui_notify(title, message):
    call_service("persistent_notification", "create", title=title, message=message)

def join_notify(target, message, title="Home Assistant"):
    call_service("notify", target, message=message, title=title)
    
def join_ring_device(target):
    call_service("joaoapps_join", "{}_ring".format(target))
    
def join_send_tasker(target, command):
    call_service("joaoapps_join", "{}_send_tasker".format(target), command=command)

def tts_say(message, media_player):
    call_service("tts", "google_say", entity_id=media_player.entity_id, message=message)
    
def lock(lock_entity):
    call_service("lock", "lock", entity_id=lock_entity.entity_id)
    
def unlock(lock_entity):
    call_service("lock", "unlock", entity_id=lock_entity.entity_id)

def turn_on(entity, **kwargs):
    if API_HANDLE is not None:
        API_HANDLE.turn_on(entity.entity_id, namespace="hass", **kwargs)
    else:
        logger.error("API Handle is None")

def toggle(entity):
    if API_HANDLE is not None:
        API_HANDLE.toggle(entity.entity_id, namespace="hass")
    else:
        logger.error("API Handle is None")

def turn_off(entity):
    if API_HANDLE:
        API_HANDLE.turn_off(entity.entity_id, namespace="hass")
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
        return API_HANDLE.anyone_home(namespace="hass")
    else:
        logger.error("API Handle is None")

def get_current_datetime():
    if API_HANDLE:
        return API_HANDLE.datetime()
    else:
        logger.error("API Handle is None")
        return None