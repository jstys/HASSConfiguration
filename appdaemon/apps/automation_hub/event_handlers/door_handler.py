from automation_hub import event_dispatcher
from automation_hub.events import door_closed_event
from automation_hub.events import door_open_event

def register_callbacks():
    event_dispatcher.register_callback(on_door_closed, DoorClosedEvent().__class__.__name__)
    event_dispatcher.register_callback(on_door_opened, DoorOpenEvent().__class__.__name__)
    
def on_door_closed(event):
    pass

def on_door_opened(event):
    pass