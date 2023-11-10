import state_machine
import timer_manager
from util import hassutil

START_TIME = "08:00:00"

def get_starttime(weekend: bool):
    if weekend:
        return "10:00:00"
    else:
        return "09:00:00"

def _disable_sleep_state():
    if state_machine.is_enabled("Sleep Mode"):
        state_machine.disable_sleep_state()

def callback():
    timer_manager.schedule_oneoff_task("disable_sleep_state", _disable_sleep_state, get_starttime(hassutil.is_weekend()))
