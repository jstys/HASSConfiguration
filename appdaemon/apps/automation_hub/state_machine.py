from util.entity_map import name_map

API_HANDLE = None

def set_api_handle(handle):
    global API_HANDLE
    API_HANDLE = handle

def disable_sleep_state():
    return API_HANDLE.set_state(name_map["sleep_mode"], state="off", namespace="hass")

def enable_sleep_state():
    return API_HANDLE.set_state(name_map["sleep_mode"], state="on", namespace="hass")

def disable_guest_state():
    return API_HANDLE.set_state(name_map["guest_mode"], state="off", namespace="hass")

def enable_guest_state():
    return API_HANDLE.set_state(name_map["guest_mode"], state="on", namespace="hass")

def is_sun_up():
    return API_HANDLE.get_state(name_map["sun"], namespace="hass") == "above_horizon"

def is_jim_home():
    return API_HANDLE.get_state(name_map["jim_presence"], namespace="hass") == "home"

def is_erica_home():
    return API_HANDLE.get_state(name_map["erica_presence"], namespace="hass") == "home"

def is_nobody_home():
    return API_HANDLE.noone_home()

def get_thermostat_mode():
    return API_HANDLE.get_state(name_map["thermostat_mode"], namespace="hass")

def is_enabled(*modes):
    return any([API_HANDLE.get_state(name_map[mode], namespace="hass") == "on" for mode in modes])
