from automation_hub import event_dispatcher
from automation_hub import state_machine
from util import logger
from events.state_machine_event import StateMachineEvent

def event_filter(event):
    return event.state == state_machine.SLEEP_STATE

def register_callbacks():
    event_dispatcher.register_callback(on_state_changed, StateMachineEvent.__name__, event_filter=event_filter)
    
def on_state_changed(event):
    if event.old == True and event.new == False:
        on_sleep_state_disabled(event)
    elif event.old == False and event.new == True:
        on_sleep_state_enabled(event)
    else:
        logger.warning("Invalid state transition for sleep state")

def on_sleep_state_enabled(event):
    logger.info("Sleep state enabled")

def on_sleep_state_disabled(event):
    logger.info("Sleep state disabled")