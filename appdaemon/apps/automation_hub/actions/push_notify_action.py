from util import hassutil
from util.entity_map import join_targets

class PushNotifyAction():
    def __init__(self):
        self._targets = []
        self._message = None
        self._title = None
        self._kwargs = {}
        
    def add_targets(self, *targets):
        for target in targets:
            self.add_target(target)
        
        return self
        
    def add_target(self, target):
        if target in join_targets:
            self._targets.append(target)
        
        return self
            
    def set_message(self, message, title="Home Assistant", **kwargs):
        self._message = message
        self._title = title
        self._kwargs = kwargs
        return self

    def notify(self):
        tts_enabled = self._kwargs.pop("tts", False)
        if tts_enabled:
            self._kwargs['tts'] = self._message
            self._kwargs['tts_language'] = "english"
        for target in self._targets:
            hassutil.join_notify(target, self._message, title=self._title, data=self._kwargs)