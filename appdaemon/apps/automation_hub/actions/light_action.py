from util.entity_map import name_map
from util import hassutil

class LightAction():
    def __init__(self):
        self._lights = []

    def add_lights(self, lights):
        for light in lights:
            self.add_light(light)

        return self

    def add_light(self, light):
        if light in name_map:
            self._lights.append(hassutil.Entity(name_map[light]))

        return self

    def turn_on(self, level=None):
        for light in self._lights:
            hassutil.turn_off_on(light, True, brightness=level)

    def turn_off(self):
        for light in self._lights:
            hassutil.turn_off_on(light, False)

    def set_level(self, level):
        for light in self._lights:
            hassutil.turn_off_on(light, True, brightness=level)

    def set_effect(self, effect):
        for light in self._lights:
            hassutil.turn_off_on(light, True, effect=effect)

    def set_color(self, color):
        for light in self._lights:
            hassutil.turn_off_on(light, True, color=color)