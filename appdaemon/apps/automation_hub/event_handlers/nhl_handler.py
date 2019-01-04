from automation_hub import event_dispatcher
from automation_hub.events import nhl_goal_event
from automation_hub.events import nhl_penalty_event
from automation_hub.events import nhl_period_start_event
from automation_hub.events import nhl_period_end_event

def register_callbacks():
    event_dispatcher.register_callback(on_nhl_goal, NHLGoalEvent().__class__.__name__)
    event_dispatcher.register_callback(on_nhl_penalty, NHLPenaltyEvent().__class__.__name__)
    event_dispatcher.register_callback(on_nhl_period_start, NHLPeriodStart().__class__.__name__)
    event_dispatcher.register_callback(on_nhl_period_end, NHLPeriodEnd().__class__.__name__)
    
def on_nhl_goal(event):
    pass

def on_nhl_penalty(event):
    pass

def on_nhl_period_start(event):
    pass

def on_nhl_period_end(event):
    pass