#!/srv/homeassistant/bin/python3
from util import hassutil

INTENT = "VacuumIntent"
_DEFAULT_VACUUM = "xiaomi_vacuum_cleaner"

def handle(api, json_message):
    action = json_message.get("MediaVerb")
    vacuum = json_message.get("VacuumName", default=_DEFAULT_VACUUM)
    if action == "start":
        api.call_service("/".join(["vacuum", "turn_on"]), entity_id=vacuum)
    elif action == "pause" or action == "resume":
        api.call_service("/".join(["vacuum", "start_pause"]), entity_id=vacuum)
    elif action == "stop":
        api.call_service("/".join(["vacuum", "stop"]), entity_id=vacuum)
    else:
        # TODO: indicate error
        pass