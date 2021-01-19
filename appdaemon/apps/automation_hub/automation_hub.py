#!/srv/homeassistant/bin/python3
import os
import importlib
import re

from util import hassutil
from util.entity_map import entity_map
from util import logutil
import appdaemon.plugins.hass.hassapi as hass
import event_factory
import event_dispatcher
import state_machine
import timer_manager
import scheduler

logger = logutil.get_logger("automation_hub")

class AutomationHub(hass.Hass):
    def initialize(self):
        hassutil.set_api_handle(self)
        timer_manager.set_api_handle(self)
        state_machine.set_api_handle(self)
        self.event_list = self.args["event_list"]
        self.subscribe_events()
        self.subscribe_states()
        if not hasattr(self, "event_handler_map"):
            self.event_handler_map = {}
        self._load_handlers()
        scheduler.schedule_daily_tasks()
        scheduler.schedule_polling_tasks()
        self._notify_started()
        
    def _load_handlers(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        handler_path = os.path.join(cwd, "event_handlers")
        ls_output = os.listdir(handler_path)
        module_files = [pyfile.replace('.py', '') for pyfile in ls_output if re.match(r'^.+\.py$', pyfile) and '__init__.py' not in pyfile]
        
        event_dispatcher.clear_callbacks()
        
        for module_name in module_files:
            if module_name in self.event_handler_map:
                module = importlib.reload(self.event_handler_map[module_name])
            else:
                module = importlib.import_module(".".join(["event_handlers", module_name]))
            module.register_callbacks()
            self.event_handler_map[module_name] = module
            
    def _notify_started(self):
        event = event_factory.create_automation_hub_started_event()
        event_dispatcher.dispatch(event)
        
    def subscribe_events(self):
        for event in self.event_list:
            self.listen_event(self.on_event, event=event, namespace="hass")
        
    def on_event(self, event_name, data, kwargs):
        logger.debug("Received New Event - name = {} data = {} kwargs = {}".format(event_name, data, kwargs))

        if event_name in self.event_list:
            
            adevent = event_factory.create_from_event(event_name, data, kwargs)
            if adevent:
                event_dispatcher.dispatch(adevent)
        else:
            logger.error(f"Received untracked event: {event_name}")
        
    def subscribe_states(self):
        for entity in entity_map.keys():
            self.listen_state(self.on_state_changed, entity=entity, attribute="all", namespace="hass")
        
    def on_state_changed(self, entity, attribute, old, new, kwargs):
        
        if entity in entity_map:
            logger.debug("Received New State Change - entity = {} attribute = {} old = {} new = {} kwargs = {}".format(entity, attribute, old, new, kwargs))
            logger.debug("Received state change for subscribed entity (name = {}, type = {}".format(entity_map[entity]['name'], entity_map[entity]['type']))
            
            friendly_name = entity_map[entity]["name"]
            entity_type = entity_map[entity]["type"]
            old_state = old.get("state") if old else None
            new_state = new.get("state") if new else None
            attributes = new.get("attributes")
            
            adevent = event_factory.create_from_state_change(friendly_name, entity_type, entity, attributes, old_state, new_state, kwargs)
            if adevent:
                event_dispatcher.dispatch(adevent)
        else:
            logger.error(f"Received untracked state change from entity: {entity}")
                
    def timer_callback(self, kwargs):
        partial = kwargs.get("partial")
        name = kwargs.get("title")
        timer_manager.remove_timer(name)
        if partial:
            partial()

    def scheduler_callback(self, kwargs):
        title = kwargs.get("title")
        partial = kwargs.get("partial")
        if partial:
            partial()