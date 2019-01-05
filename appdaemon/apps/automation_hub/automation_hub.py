#!/srv/homeassistant/bin/python3
import os
import importlib
import re

import appdaemon.plugins.hass.hassapi as hass
import event_factory
import event_dispatcher
import logger

class AutomationHub(hass.Hass):
    def initialize(self):
        self.entity_map = self.args["entity_map"]
        self.event_list = self.args["event_list"]
        self.setup_logger()
        self.subscribe_events()
        self.subscribe_states()
        self.event_handlers = []
        self._load_handlers()
        
    def _load_handlers(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        handler_path = os.path.join(cwd, "event_handlers")
        ls_output = os.listdir(handler_path)
        module_files = [pyfile for pyfile in ls_output if re.match(r'^.+\.py$', pyfile) and '__init__.py' not in pyfile]
        
        event_dispatcher.clear_callbacks()
        
        for module_name in module_files:
            module = importlib.import_module(".".join(["event_handlers", module_name.replace('.py', '')]))
            module.register_callbacks()
            self.event_handlers.append(module)

    def _reload_handlers(self):
        event_dispatcher.clear_callbacks()
        reloaded_handlers = []
        for module in self.event_handlers:
            reloaded = importlib.reload(module)
            reloaded.register_callbacks()
            reloaded_handlers.append(reloaded)
            
        self.event_handlers = reloaded_handlers
    
    def setup_logger(self):
        log = self.get_main_log()
        logger.set_logger(log)
    
    def subscribe_events(self):
        self.listen_event(self.on_event)
        
    def on_event(self, event_name, data, kwargs):
        if event_name in self.event_list:
            logger.info("Received New Event - name = {} data = {} kwargs = {}".format(event_name, data, kwargs))
            
            adevent = event_factory.create_from_event(event_name, data, kwargs)
            if adevent:
                event_dispatcher.dispatch(adevent)
        
    def subscribe_states(self):
        self.listen_state(self.on_state_changed)
        
    def on_state_changed(self, entity, attribute, old, new, kwargs):
        
        if entity in self.entity_map:
            logger.info("Received New State Change - entity = {} attribute = {} old = {} new = {} kwargs = {}".format(entity, attribute, old, new, kwargs))
            logger.info("Received state change for subscribed entity (name = {}, type = {}".format(self.entity_map[entity]['name'], self.entity_map[entity]['type']))
            
            friendly_name = self.entity_map[entity]["name"]
            entity_type = self.entity_map[entity]["type"]
            
            adevent = event_factory.create_from_state_change(friendly_name, entity_type, entity, attribute, old, new, kwargs)
            if adevent:
                event_dispatcher.dispatch(adevent)