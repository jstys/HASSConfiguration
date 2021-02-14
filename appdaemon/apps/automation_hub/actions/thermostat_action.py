from util.entity_map import name_map
from util import hassutil
from util import logutil

logger = logutil.get_logger("automation_hub")

class ThermostatAction():
    def __init__(self):
        self._thermostats = []

    def add_thermostats(self, thermostats):
        for thermostat in thermostats:
            self.add_thermostat(thermostat)

        return self

    def add_thermostat(self, thermostat):
        if thermostat in name_map:
            self._thermostats.append(hassutil.Entity(name_map[thermostat]))
        else:
            logger.error("Unable to add unknown thermostat to ThermostatAction: {}".format(thermostat))

        return self

    def turn_on(self):
        for thermostat in self._thermostats:
            hassutil.turn_on(thermostat)

    def turn_off(self):
        for thermostat in self._thermostats:
            hassutil.turn_off(thermostat)

    def set_temperature(self, temperature, hvac_mode):
        for thermostat in self._thermostats:
            hassutil.call_service("climate", "set_temperature", entity_id=thermostat.entity_id, temperature=temperature, hvac_mode=hvac_mode)
            hassutil.call_service("climate", "set_hvac_mode", entity_id=thermostat.entity_id, hvac_mode=hvac_mode)

    def set_hvac_mode(self, hvac_mode):
        for thermostat in self._thermostats:
            hassutil.call_service("climate", "set_hvac_mode", entity_id=thermostat.entity_id, hvac_mode=hvac_mode)