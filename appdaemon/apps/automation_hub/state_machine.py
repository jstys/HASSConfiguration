from actions.event_action import EventAction
from util import logger

state_map = {}

SLEEP_STATE = "sleep"
GUEST_STATE = "guest"
SUN_UP_STATE = "sun"
JIM_HOME_STATE = "jim_home"
ERICA_HOME_STATE = "erica_home"
NOBODY_HOME_STATE = "nobody_home"
THERMOSTAT_STATE = "thermostat_state"
CHRISTMAS_STATE = "christmas_state"

def set_state(state, new_value):
    global state_map

    old_value = state_map.get(state)

    logger.info("Setting {} from old:{} to new:{}".format(state, old_value, new_value))

    state_map[state] = new_value

    if old_value != new_value:
        EventAction().fire("state_machine.state_changed", state=state, old=old_value, new=new_value)

def get_state(state):
    return state_map.get(state)

