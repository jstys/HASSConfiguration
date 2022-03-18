import state_machine

def get_starttime(is_weekend: bool):
    if is_weekend:
        return "10:00:00"
    else:
        return "09:00:00"

def callback():
    if state_machine.is_enabled("sleep_mode"):
        state_machine.disable_sleep_state()
