from automation_hub import event_dispatcher
from automation_hub import state_machine
from util import logger
from events.presence_event import PresenceEvent
from actions.push_notify_action import PushNotifyAction

def register_callbacks():
    event_dispatcher.register_callback(on_presence_changed, PresenceEvent.__name__)
    
def on_presence_changed(event):
    if event.old == "home" and event.new == "not_home":
        on_person_home(event.name)
    elif event.old == "not_home" and event.new == "home":
        on_person_away(event.name)

def on_person_away(name):
    logger.info("{} has left home".format(name))
    
    if name == "jim_presence":
        PushNotifyAction().add_target("jim_cell_notify").set_message("Come back soon!").notify()


def on_person_home(name):
    logger.info("{} has arrived home".format(name))
    
    if name == "jim_presence":
        PushNotifyAction().add_target("jim_cell_notify").set_message("Welcome home!").notify()
        