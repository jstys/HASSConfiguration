from util.entity_map import name_map
from util import hassutil
from util import logger

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
        else:
            logger.error("Unable to add unknown light to LightAction: {}".format(light))

        return self

    def turn_on(self, level=None):
        for light in self._lights:
            hassutil.turn_on(light, brightness_pct=level)

    def turn_off(self):
        for light in self._lights:
            hassutil.turn_off(light)

    def set_level(self, level):
        for light in self._lights:
            hassutil.set_level(light, brightness_pct=level)

    def set_effect(self, effect):
        for light in self._lights:
            hassutil.set_light_effect(light, effect=effect)

    def set_color(self, color):
        for light in self._lights:
            hassutil.set_light_color(light, color_name=color)