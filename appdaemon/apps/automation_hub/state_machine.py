from util.entity_map import name_map
from util import  hassutil

def disable_sleep_state():
    return hassutil.turn_off(hassutil.Entity(name_map["sleep_mode"]))

def enable_sleep_state():
    return hassutil.turn_on(hassutil.Entity(name_map["sleep_mode"]))

def disable_guest_state():
    return hassutil.turn_off(hassutil.Entity(name_map["guest_mode"]))

def enable_guest_state():
    return hassutil.turn_on(hassutil.Entity(name_map["guest_mode"]))

def is_sun_up():
    return hassutil.get_state(hassutil.Entity(name_map["sun"])) == "above_horizon"

def is_jim_home():
    return hassutil.get_state(hassutil.Entity(name_map["jim_presence"])) == "home"

def is_erica_home():
    return hassutil.get_state(hassutil.Entity(name_map["erica_presence"])) == "home"

def is_heating_enabled():
    return hassutil.get_state(hassutil.Entity(name_map["thermostat_mode"])).lower() == "heating"

def is_cooling_enabled():
    return hassutil.get_state(hassutil.Entity(name_map["thermostat_mode"])).lower() == "cooling"

def is_garage_open():
    return hassutil.get_state(hassutil.Entity(name_map["garage_door"])).lower() == "open"

def is_enabled(*modes):
    return any([hassutil.get_state(hassutil.Entity(name_map[mode])) == "on" for mode in modes])

def get_number(number_setting):
    return hassutil.get_state(hassutil.Entity(name_map[number_setting]))