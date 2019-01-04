from automation_hub import event_dispatcher
from automation_hub.events.motion_triggered_event import MotionTriggeredEvent
from automation_hub.events.motion_cleared_event import MotionClearedEvent
from automation_hub import logger

def register_callbacks():
    event_dispatcher.register_callback(on_motion_triggered, MotionTriggeredEvent().__class__.__name__)
    event_dispatcher.register_callback(on_motion_cleared, MotionClearedEvent().__class__.__name__)
    
def on_motion_triggered(event):
    if event.name == "hallway_motion_sensor":
        hallway_motion(event)

def on_motion_cleared(event):
    if event.name == "hallway_motion_sensor":
        hallway_cleared(event)
    
def hallway_motion(event):
    logger.log("Hallway motion detected")

def hallway_cleared(event):
    logger.log("Hallway motion cleared")