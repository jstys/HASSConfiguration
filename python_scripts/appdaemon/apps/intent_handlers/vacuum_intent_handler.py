#!/srv/homeassistant/bin/python3
from util.hass_util import Entity, call_service

INTENT = "VacuumIntent"
_DEFAULT_VACUUM = "xiaomi_vacuum_cleaner"

def handle(api, json_message, *args, **kwargs):
    action = json_message.get("MediaVerb")
    vacuum = Entity.fromSplitName("vacuum", json_message.get("VacuumName", _DEFAULT_VACUUM))
    if action == "start":
        call_service(api, "vacuum", "turn_on", entity_id=vacuum.entity_id)
    elif action == "pause" or action == "resume":
        call_service(api, "vacuum", "start_pause", entity_id=vacuum.entity_id)
    elif action == "stop":
        call_service(api, "vacuum", "return_to_base", entity_id=vacuum.entity_id)
    else:
        # TODO: indicate error
        pass
