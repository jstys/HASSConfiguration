from automation_hub import event_dispatcher
from automation_hub import state_machine
from events.nhl_goal_event import NHLGoalEvent
from events.nhl_penalty_event import NHLPenaltyEvent
from events.nhl_period_start_event import NHLPeriodStartEvent
from events.nhl_period_end_event import NHLPeriodEndEvent
from events.nhl_game_end_event import NHLGameEndEvent
from actions.tts_action import TTSAction

def register_callbacks():
    event_dispatcher.register_callback(on_nhl_goal, NHLGoalEvent.__name__)
    event_dispatcher.register_callback(on_nhl_penalty, NHLPenaltyEvent.__name__)
    event_dispatcher.register_callback(on_nhl_period_start, NHLPeriodStartEvent.__name__)
    event_dispatcher.register_callback(on_nhl_period_end, NHLPeriodEndEvent.__name__)
    event_dispatcher.register_callback(on_nhl_game_end, NHLGameEndEvent.__name__)
    
def on_nhl_goal(event):
    if not state_machine.is_enabled("sleep_mode"):
        speech = f"{event.team} goal scored by number {event.scorer_number}, {event.scorer}."
        if event.primary_assist:
            speech = speech + f" Assisted by number {event.primary_number}, {event.primary_assist}"
        if event.secondary_assist:
            speech = speech + f" and number {event.secondary_number}, {event.secondary_assist}"
        TTSAction().add_assistant("living_room").say(speech)

def on_nhl_penalty(event):
    if not state_machine.is_enabled("sleep_mode"):
        speech = f"{event.team} penalty on number {event.number}, {event.player}.  "
        speech = speech + f"{event.duration} minute {event.severity} for {event.penalty}."
        TTSAction().add_assistant("living_room").say(speech)

def on_nhl_game_end(event):
    if not state_machine.is_enabled("sleep_mode"):
        TTSAction().add_assistant("living_room").say("The game has ended")

def on_nhl_period_start(event):
    if not state_machine.is_enabled("sleep_mode"):
        TTSAction().add_assistant("living_room").say("Start of {}".format(_get_period_num(event.period)))

def on_nhl_period_end(event):
    if not state_machine.is_enabled("sleep_mode"):
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
