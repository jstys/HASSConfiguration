from util import hassutil
from util import trello_util

INTENT = "ListIntent"

def handle(api, json_message, received_room, *args, **kwargs):
    list_type = json_message.get("ListType")
    if list_type.lower() in ["grocery", "groceries"]:
        handle_grocery_list(api, json_message, received_room)

def handle_grocery_list(api, json_message, received_room):
    add_item = json_message.get("ListItemAdd")
    remove_item = json_message.get("ListItemRemove")

    if remove_item:
        trello_util.remove_from_grocery_list(remove_item)
    elif add_item:
        trello_util.add_to_grocery_list(add_item)