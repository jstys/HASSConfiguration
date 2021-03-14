from util import hassutil
from util.entity_map import join_targets

class JoinAction():
    def __init__(self):
        self._targets = []
        self._message = None
        self._title = None
        
    def add_targets(self, *targets):
        for target in targets:
            self.add_target(target)
        
        return self
        
    def add_target(self, target):
        if target in join_targets:
            self._targets.append(target)
        
        return self

    def send_taker_command(self, command):
        for target in self._targets:
            hassutil.join_send_tasker(target, command)

    def ring(self):
        for target in self._targets:
            hassutil.join_ring_device(target)