#!/srv/homeassistant/bin/python3
import logging

import appdaemon.plugins.hass.hassapi as hass

class AutomationHub(hass.Hass):
    def initialize(self):
        self.entity_map = self.args["entity_map"]
        self.event_list = self.args["event_list"]
        self.setup_logger()
        self.subscribe_events()
        self.subscribe_states()
    
    def setup_logger(self):
        log = self.get_main_log()
        FORMAT = "[%(filename)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=FORMAT)
    
    def subscribe_events(self):
        self.listen_event(self.on_event)
        
    def on_event(self, event_name, data, kwargs):
        if event_name in self.event_list:
            self.log("Received New Event - name = {} data = {} kwargs = {}".format(event_name, data, kwargs))
        
    def subscribe_states(self):
        self.listen_state(self.on_state_changed)
        
    def on_state_changed(self, entity, attribute, old, new, kwargs):
        
        if entity in self.entity_map:
            self.log("Received New State Change - entity = {} attribute = {} old = {} new = {} kwargs = {}".format(entity, attribute, old, new, kwargs))
            self.log("Received state change for subscribed entity (name = {}, type = {}".format(self.entity_map[entity]['name'], self.entity_map[entity]['type']))