from automation_hub import event_dispatcher
from util import logger
from util import hassutil
from util import trello_util
from util.entity_map import name_map
from events.generate_mealplan_event import GenerateMealplanEvent
from events.archive_mealplan_event import ArchiveMealplanEvent

# Read HASS secrets
secrets = hassutil.read_config_file(hassutil.SECRETS)
trello_util.set_auth(secrets["trello_key"], secrets["trello_secret"], secrets["trello_oauth"])

def register_callbacks():
    event_dispatcher.register_callback(on_generate, GenerateMealplanEvent.__name__)
    event_dispatcher.register_callback(on_archive, ArchiveMealplanEvent.__name__)
    
def on_generate(event):
    success, errorList = trello_util.generate_grocery_list_from_meal_plan()
    if not success:
        hassutil.gui_notify("Grocery List Errors", message="\n".join(errorList))

def on_archive(event):
    trello_util.archive_last_week()