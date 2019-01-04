from automation_hub import event_dispatcher
from automation_hub.events.nhl_goal_event import NHLGoalEvent
from automation_hub.events.nhl_penalty_event import NHLPenaltyEvent
from automation_hub.events.nhl_period_start_event import NHLPeriodStartEvent
from automation_hub.events.nhl_period_end_event import NHLPeriodEndEvent

def register_callbacks():
    event_dispatcher.register_callback(on_nhl_goal, NHLGoalEvent().__class__.__name__)
    event_dispatcher.register_callback(on_nhl_penalty, NHLPenaltyEvent().__class__.__name__)
    event_dispatcher.register_callback(on_nhl_period_start, NHLPeriodStartEvent().__class__.__name__)
    event_dispatcher.register_callback(on_nhl_period_end, NHLPeriodEndEvent().__class__.__name__)
    
def on_nhl_goal(event):
    pass

def on_nhl_penalty(event):
    pass

def on_nhl_period_start(event):
    pass

def on_nhl_period_end(event):
    pass