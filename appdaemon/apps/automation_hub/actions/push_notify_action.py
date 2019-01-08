from util import hassutil
from util.entity_map import name_map

class PushNotifyAction():
    def __init__(self):
        self._targets = []
        self._message = None
        self._title = None
        
    def add_targets(self, targets):
        for target in targets:
            self.add_target(target)
        
        return self
        
    def add_target(self, target):
        if target in name_map:
            self._targets.append(hassutil.Entity(name_map[target]).entity_id)
        
        return self
            
    def set_message(self, message, title="Home Assistant"):
        self._message = message
        self._title = title
        return self

    def notify(self):
        for target in self._targets:
            hassutil.join_notify(target, self._message, title=self._title)