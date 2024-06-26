from datetime import date
import os
from typing import List

import yaml
import api_handle
from util import logger

APPD_DIR = "/conf"
SECRETS = os.path.join(APPD_DIR, "secrets.yaml")
ENTITY_MAP = os.path.join(APPD_DIR, "apps", "util", "entity_map.yaml")

class Entity(object):
    def __init__(self, fully_qualified_name):
        fqn_split = fully_qualified_name.split(".")
        self.domain = fqn_split[0].strip()
        self.name = fqn_split[1].strip()
        self.entity_id = fully_qualified_name

    @classmethod
    def fromSplitName(cls, domain, name):
        return cls(".".join([domain, name]))

def read_config_file(filename):
    try:
        with open(filename) as yamlfile:
            return yaml.safe_load(yamlfile)
    except Exception as e:
        logger.error(f"Error Loading {filename}: {e}")
        return {}

def read_binary_file(filename):
    with open(filename, "rb") as binary_file:
        return binary_file.read()

def gui_notify(title, message, notification_id=None):
    if notification_id:
        call_service("persistent_notification", "create", title=title, message=message, notification_id=notification_id)
    else:
        call_service("persistent_notification", "create", title=title, message=message)

def join_notify(target, message, title="Home Assistant", **kwargs):
    call_service("notify", target, message=message, title=title, **kwargs)

def discord_notify(channel_ids: List[str], message, title="Home Assistant Bot", **kwargs):
    call_service("notify", "hass", target=channel_ids, message=message, title=title, **kwargs)
    
def join_ring_device(target):
    call_service("joaoapps_join", "{}_ring".format(target))
    
def join_send_tasker(target, command):
    call_service("joaoapps_join", "{}_send_tasker".format(target), command=command)

def tts_say(message, media_player: Entity):
    call_service("tts", "speak", entity_id="tts.google_en_com", media_player_entity_id=media_player.entity_id, message=message)
    
def lock(lock_entity: Entity):
    call_service("lock", "lock", entity_id=lock_entity.entity_id)
    
def unlock(lock_entity: Entity):
    call_service("lock", "unlock", entity_id=lock_entity.entity_id)

def activate_scene(name: str):
    call_service("scene", "turn_on", entity_id=f"scene.{'_'.join(name.lower().split())}")

def turn_on(entity: Entity, **kwargs):
    try_api_call("turn_on", entity.entity_id, namespace="hass", **kwargs)

def toggle(entity: Entity):
    try_api_call("toggle", entity.entity_id, namespace="hass")

def turn_off(entity: Entity):
    try_api_call("turn_off", entity.entity_id, namespace="hass")

def call_service(domain, action, **kwargs):
    try_api_call("call_service", "/".join([domain, action]), namespace="hass", **kwargs)

def fire_event(event, **kwargs):
    try_api_call("fire_event", event, namespace="hass", **kwargs)

def get_state(entity: Entity, **kwargs):
    return try_api_call("get_state", entity.entity_id, namespace="hass", **kwargs)

def set_state(entity: Entity, state, **kwargs):
    return try_api_call("set_state", entity.entity_id, state=state, namespace="hass", **kwargs)

def is_someone_home():
    return try_api_call("anyone_home", person=True, namespace="hass")

def is_nobody_home():
    return try_api_call("noone_home", person=True, namespace="hass")

def get_current_datetime():
    return try_api_call("datetime")

def get_current_date() -> date:
    return try_api_call("date")

def is_weekend():
    return get_current_date().weekday() > 4

def try_api_call(func_name, *args, **kwargs):
    try:
        func = getattr(api_handle.instance, func_name)
        return func(*args, **kwargs)
    except AttributeError as attrib_err:
        logger.error(f"Attribute Error: {attrib_err} while running {func_name}")
    except TimeoutError as timeout_err:
        logger.error(f"Timeout Error: {timeout_err} while running {func_name}")
    except Exception as other_err:
        logger.error(f"Other Error: {other_err} while running {func_name}")
