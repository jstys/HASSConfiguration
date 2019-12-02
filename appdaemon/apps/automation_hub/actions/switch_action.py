from util.entity_map import name_map
from util import hassutil
from util import logger

class SwitchAction():
    def __init__(self):
        self._switches = []

    def add_switches(self, switches):
        for switch in switches:
            self.add_switch(switch)

        return self

    def add_switch(self, switch):
        if switch in name_map:
            self._switches.append(hassutil.Entity(name_map[switch]))
        else:
            logger.error("Unable to add unknown switch to switchAction: {}".format(switch))

        return self

    def toggle(self):
        for switch in self._switches:
            hassutil.toggle(switch)

    def turn_on(self):
        for switch in self._switches:
            hassutil.turn_on(switch)

    def turn_off(self):
        for switch in self._switches:
            hassutil.turn_off(switch)
