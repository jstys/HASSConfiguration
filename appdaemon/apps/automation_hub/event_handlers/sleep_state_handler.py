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

def event_filter(event):
    return event.name == "sleep_mode"

def register_callbacks():
    event_dispatcher.register_callback(on_state_changed, InputEvent.__name__, event_filter=event_filter)
    
def on_state_changed(event):
    if event.old == "on" and event.new == "off":
        on_sleep_state_disabled(event)
    elif event.old == "off" and event.new == "on":
        on_sleep_state_enabled(event)
    else:
        logger.warning("Invalid state transition for sleep state")

def on_sleep_state_enabled(event):
    logger.info("Sleep state enabled")

    state_machine.set_state(state_machine.SLEEP_STATE, True)
    
    DoorLockAction().add_lock("front_entrance_lock").lock()
    LightAction().add_light("manual_off_lights").turn_off()
    VacuumAction().add_vacuum("robot_vacuum").start()
    assistant_action = AssistantAction().add_assistant("master_bedroom")
    assistant_action.disable_hotword()
    assistant_action.disable_led()

def on_sleep_state_disabled(event):
    logger.info("Sleep state disabled")
    
    state_machine.set_state(state_machine.SLEEP_STATE, False)

    assistant_action = AssistantAction().add_assistant("master_bedroom")
    assistant_action.enable_hotword()
    assistant_action.enable_led()