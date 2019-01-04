from automation_hub import event_dispatcher
from automation_hub.events import motion_triggered_event
from automation_hub.events import motion_cleared_event

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent().__class__.__name__)
    event_dispatcher.register_callback(on_motion_cleared, MotionClearedEvent().__class__.__name__)
    
def on_motion_triggered(event):
    pass

def on_motion_cleared(event):
    pass