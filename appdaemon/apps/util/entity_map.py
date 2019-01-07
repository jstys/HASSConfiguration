entity_map = {
    "binary_sensor.water_leak_sensor_158d00023a58df": {
        "name": "basement_water_sensor",
        "type": "water_sensor"
    },
    "binary_sensor.motion_sensor_158d00016612a5": {
        "name": "hallway_motion_sensor",
        "type": "motion_sensor"
    },
    "binary_sensor.front_door_sensor": {
        "name": "front_door_sensor",
        "type": "door_sensor"
    },
    "binary_sensor.garage_sensor": {
        "name": "garage_door_sensor",
        "type": "door_sensor"
    },
    "binary_sensor.door_window_sensor_158d0001d3a024": {
        "name": "kitchen_fridge_sensor",
        "type": "door_sensor"
    },
    "binary_sensor.switch_158d00016da2c9": {
        "name": "living_room_button",
        "type": "button"
    },
    "binary_sensor.switch_158d00016dbf86": {
        "name": "master_bedroom_button",
        "type": "button"
    },
    "media_player.living_room_tv": {
        "name": "living_room_tv",
        "type": "tv",
        "room": "living_room",
        "floor": "first"
    },
    "media_player.master_bedroom_tv": {
        "name": "master_bedroom_tv",
        "type": "tv",
        "room": "master_bedroom",
        "floor": "second"
    },
    "light.master_bedroom_fixture": {
        "name": "master_bedroom_fixture",
        "type": "light",
        "room": "master_bedroom",
        "floor": "second"
    },
    "light.living_room_lamps": {
        "name": "living_room_lamps",
        "type": "light",
        "room": "living_room",
        "floor": "first"
    },
    "light.hallway_lights": {
        "name": "hallway_lights",
        "type": "light",
        "room": "hallway",
        "floor": "second"
    },
    "light.porch_light": {
        "name": "porch_light",
        "type": "light",
        "room": "porch",
        "floor": "first"
    },
    "light.basement_staircase_light": {
        "name": "landing_light",
        "type": "light",
        "room": "landing",
        "floor": "basement"
    },
    "light.kitchen_lights": {
        "name": "kitchen_lights",
        "type": "light",
        "room": "kitchen",
        "floor": "first"
    },
    "zwave.linear_wa00z1_scene_switch": {
        "name": "staircase_bottom_switch",
        "type": "switch"
    },
    "zwave.linear_wa00z1_scene_switch_2": {
        "name": "staircase_top_switch",
        "type": "switch"
    },
    "lock.assa_abloy_yale_push_button_deadbolt_yrd110_locked_4": {
        "name": "front_door_lock",
        "type": "lock"
    }
}

name_map = {}

for entity_id, mapped in entity_map.items():
    name_map[mapped["name"]] = entity_id