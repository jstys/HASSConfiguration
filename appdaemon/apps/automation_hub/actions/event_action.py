from util import hassutil

class EventAction():
    def __init__(self):
        pass

    def fire(self, event, **kwargs):
        hassutil.fire_event(event, **kwargs)