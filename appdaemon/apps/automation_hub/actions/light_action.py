from util.entity_map import name_map
from util import hassutil
from util import logutil

logger = logutil.get_logger("automation_hub")

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

    def toggle(self):
        for light in self._lights:
            hassutil.toggle(light)

    def turn_on(self, brightness_pct=100, **kwargs):
        for light in self._lights:
            hassutil.turn_on(light, brightness_pct=brightness_pct, **kwargs)

    def turn_on_no_brightness(self, **kwargs):
        for light in self._lights:
            hassutil.turn_on(light, **kwargs)

    def turn_off(self):
        for light in self._lights:
            hassutil.turn_off(light)