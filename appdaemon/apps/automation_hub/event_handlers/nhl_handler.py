from automation_hub import event_dispatcher
from automation_hub import state_machine
from events.nhl_goal_event import NHLGoalEvent
from events.nhl_penalty_event import NHLPenaltyEvent
from events.nhl_period_start_event import NHLPeriodStartEvent
from events.nhl_period_end_event import NHLPeriodEndEvent
from actions.tts_action import TTSAction

def register_callbacks():
    event_dispatcher.register_callback(on_nhl_goal, NHLGoalEvent.__name__)
    event_dispatcher.register_callback(on_nhl_penalty, NHLPenaltyEvent.__name__)
    event_dispatcher.register_callback(on_nhl_period_start, NHLPeriodStartEvent.__name__)
    event_dispatcher.register_callback(on_nhl_period_end, NHLPeriodEndEvent.__name__)
    
def on_nhl_goal(event):
    pass

def on_nhl_penalty(event):
    pass

def on_nhl_period_start(event):
    if not state_machine.get_state(state_machine.SLEEP_STATE):
        TTSAction().add_assistant("living_room").say("Start of {}".format(_get_period_num(event.period)))

def on_nhl_period_end(event):
    if not state_machine.get_state(state_machine.SLEEP_STATE):
        TTSAction().add_assistant("living_room").say("End of {}".format(_get_period_num(event.period)))

def _get_period_num(num):
    if num == 1:
        return "the 1st period"
    elif num == 2:
        return "the 2nd period"
    elif num == 3:
        return "the 3rd period"
    elif num > 3:
        return "Overtime"
