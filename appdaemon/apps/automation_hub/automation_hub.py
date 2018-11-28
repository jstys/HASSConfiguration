#!/srv/homeassistant/bin/python3
import appdaemon.plugins.hass.hassapi as hass

class AutomationHub(hass.Hass):
    def initialize(self):
        pass