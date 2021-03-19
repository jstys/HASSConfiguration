from functools import partial

import event_dispatcher
import timer_manager
from util import logutil
from events.unavailable_event import UnavailableEvent
from actions.push_notify_action import PushNotifyAction

logger = logutil.get_logger("automation_hub")

def register_callbacks():
    event_dispatcher.register_callback(on_unavailable, UnavailableEvent.__name__)

def on_available(event):
    logger.info(f"Received available for {event.name}")
    timer_manager.cancel_timer(f"{event.name}_unavailable_timer")
    
def on_unavailable(event):
    logger.info(f"Received unavailable for {event.name}")
    timer_manager.start_timer(f"{event.name}_unavailable_timer", partial(on_timeout, event.name), minutes=5)

def on_timeout(friendly_name):
    PushNotifyAction().add_target("jim_cell").set_message(f"{friendly_name} is unavailable").notify()