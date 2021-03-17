import event_dispatcher
from util import logutil
from events.unavailable_event import UnavailableEvent
from actions.push_notify_action import PushNotifyAction

logger = logutil.get_logger("automation_hub")

def register_callbacks():
    event_dispatcher.register_callback(on_unavailable, UnavailableEvent.__name__)
    
def on_unavailable(event):
    logger.info(f"Received unavailable for {event.name}")
    PushNotifyAction().add_target("jim_cell").set_message(f"{event.name} is unavailable").notify()