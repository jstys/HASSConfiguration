from automation_hub import event_dispatcher
from automation_hub import state_machine
from util import entity_map
from util import logger
from util import hassutil
from events.input_event import InputEvent
from actions.door_lock_action import DoorLockAction
from actions.vacuum_action import VacuumAction
from actions.light_action import LightAction
from actions.assistant_action import AssistantAction
from actions.join_action import JoinAction

def event_filter(event):
    return event.name == "guest_mode"

def register_callbacks():
    event_dispatcher.register_callback(on_state_changed, InputEvent.__name__, event_filter=event_filter)
    
def on_state_changed(event):
    if event.old == "on" and event.new == "off":
        on_guest_state_disabled(event)
    elif event.old == "off" and event.new == "on":
        on_guest_state_enabled(event)
    else:
        logger.warning("Invalid state transition for guest state")

def on_guest_state_enabled(event):
    logger.info("Guest state enabled")

    state_machine.set_state(state_machine.GUEST_STATE, True)

def on_guest_state_disabled(event):
    logger.info("Guest state disabled")
    
    state_machine.set_state(state_machine.SLEEP_STATE, False)