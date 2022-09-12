import event_dispatcher
from util import logger
from events.automation_hub_started_event import AutomationHubStartedEvent

def register_callbacks():
    event_dispatcher.register_callback(on_start, AutomationHubStartedEvent.__name__)
    
def on_start(event):
    logger.info("Automation Hub Started")
