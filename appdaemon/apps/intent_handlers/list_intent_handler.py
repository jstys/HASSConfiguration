from util.hassutil import tts_say
from util import trello_util

INTENT = "ListIntent"

def handle(api, json_message, received_room, *args, **kwargs):
    list_type = json_message.get("ListType")
    if list_type.lower() in ["grocery", "groceries"]:
        handle_grocery_list(api, json_message, received_room)

def handle_grocery_list(api, json_message, received_room):
    add_item = json_message.get("ListItemAdd")
    remove_item = json_message.get("ListItemRemove")
    result = False
    message = None

    if remove_item:
        result, message = trello_util.remove_from_grocery_list(remove_item)
    elif add_item:
        result, message = trello_util.add_to_grocery_list(add_item)
        
    if message:
        tts_say(api, message, received_room)