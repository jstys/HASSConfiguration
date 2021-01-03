import event_dispatcher
import state_machine
from util import logutil
from events.automation_hub_started_event import AutomationHubStartedEvent

logger = logutil.get_logger("automation_hub")

def register_callbacks():
    event_dispatcher.register_callback(on_start, AutomationHubStartedEvent.__name__)
    
def on_start(event):
    logger.info("Automation Hub Started")
