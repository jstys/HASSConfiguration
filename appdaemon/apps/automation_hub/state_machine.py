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

def is_heating_enabled():
    return API_HANDLE.get_state(name_map["thermostat_mode"], namespace="hass").lower() == "heating"

def is_cooling_enabled():
    return API_HANDLE.get_state(name_map["thermostat_mode"], namespace="hass").lower() == "cooling"

def is_garage_open():
    return API_HANDLE.get_state(name_map["garage_door"], namespace="hass").lower() == "open"

def is_enabled(*modes):
    return any([API_HANDLE.get_state(name_map[mode], namespace="hass") == "on" for mode in modes])

def get_number(number_setting):
    return API_HANDLE.get_state(name_map[number_setting], namespace="hass")

def set_state(entity_name, state):
    attributes = API_HANDLE.get_state(name_map[entity_name], attribute="all", namespace="hass").get("attributes", {})
    return API_HANDLE.set_state(name_map[entity_name], state=state, attributes=attributes, namespace="hass")