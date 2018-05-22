from functools import partial

from util.hassutil import tts_say, pushbullet_notify, gui_notify
from util import trello_util

INTENT = "ListIntent"

def initialize(api):
    api.listen_event(partial(on_archive_mealplan, api), "archive_mealplan")
    api.listen_event(partial(on_generate_mealplan, api), "generate_mealplan")

def on_archive_mealplan(api, event, data, kwargs):
    api.log("on_archive_mealplan")
    _archive_mealplan()

def on_generate_mealplan(api, event, data, kwargs):
    api.log("on_generate_mealplan")
    _generate_grocery_list(api)

def handle(api, json_message, received_room, *args, **kwargs):
    list_type = json_message.get("ListType")
    if list_type.lower() in ["grocery", "groceries"]:
        handle_grocery_list(api, json_message, received_room)

def handle_grocery_list(api, json_message, received_room):
    add_item = json_message.get("ListItemAdd")
    remove_item = json_message.get("ListItemRemove")
    generate = json_message.get("ListGenerate")
    message = None

    if remove_item:
        _, message = _remove_item(remove_item)
    elif add_item:
        _, message = _add_item(add_item)
    elif generate:
        _, message = _generate_grocery_list(api)

    if message:
        tts_say(api, message, received_room)
        
def _add_item(item):
    return trello_util.add_to_grocery_list(item)

def _remove_item(item):
    return trello_util.remove_from_grocery_list(item)

def _generate_grocery_list(api):
    result, message = trello_util.generate_grocery_list_from_meal_plan()
    if not result and message:
        pushbullet_notify(api, account="jim_pushbullet", devices=["device/jim_cell"], title="list_intent_handler", message=message)
        gui_notify(api, title="list_intent_handler", message=message)
    
    return (result, message)

def _archive_mealplan():
    return trello_util.archive_last_week()
