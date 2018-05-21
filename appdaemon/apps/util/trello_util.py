import requests
import re
from requests_oauthlib import OAuth1
from util import hassutil

API_BASE = "https://api.trello.com/1/"
CHECKED_STATE = "complete"
UNCHECKED_STATE = "incomplete"

_AUTH = None
_DAY_LIST_MAP = {
    "Sunday": "55e52c3cb60dbb6c3f272344",
    "Monday": "55e52c292ccf879bc4a55b95",
    "Tuesday": "55e52c31d5031bdd77a749eb",
    "Wednesday": "55e52c35f92f640d27dacd19",
    "Thursday": "55fdfbdc374a4850b88dd741",
    "Friday": "55fdfbeda2454c5f70e8bd88",
    "Saturday": "562af24f75a935532aed4546"
}
_GROCERY_LIST_ID = "1iKTzp7F"

def generate_grocery_list_from_meal_plan():
    failed_to_add = []

    for day, _ in _DAY_LIST_MAP.items():
        for item in _get_grocery_items_for_day(day):
            result, _ = add_to_grocery_list(_get_grocery_item_name(item), _get_grocery_item_amount(item))
            if not result:
                failed_to_add.append(_get_grocery_item_name(item))

    if failed_to_add:
        return False, "Failed to add the following items: {}".format(",".join(failed_to_add))
    else:
        return True, "Successfully generated grocery list"

def add_to_grocery_list(item_name, amount=""):
    item = _get_item_reference_from_grocery_list(item_name, _get_grocery_list())
    if item:
        _update_item_amount(item, amount)
        item["state"] = UNCHECKED_STATE
        _save_item(item)
        return True, " ".join([item_name, "added to the grocery list"])
    else:
        return False, " ".join([item_name, "is not on the grocery list"])

def remove_from_grocery_list(item_name):
    item = _get_item_reference_from_grocery_list(item_name, _get_grocery_list())
    if item:
        _update_item_amount(item, "")
        item["state"] = CHECKED_STATE
        _save_item(item)
        return True, " ".join([item_name, "removed from the grocery list"])
    else:
        return False, " ".join([item_name, "is not on the grocery list"])

def reset_all_item_amounts():
    grocery_json = _get_grocery_list()
    for category in grocery_json:
        for grocery_item in category.get("checkItems"):
            _update_item_amount(grocery_item, "")
            _save_item(grocery_item)

def _load_auth():
    secrets = hassutil.read_config_file(hassutil.SECRETS)
    if secrets:
        try:
            return OAuth1(secrets['trello_key'], secrets['trello_secret'], secrets['trello_oauth'])
        except KeyError:
            pass

    return None

def _get_day_list(day):
    if _DAY_LIST_MAP.get(day.title) is not None:
        return requests.get()

def _get_item_reference_from_grocery_list(item, grocery_json):
    for category in grocery_json:
        for grocery_item in category.get("checkItems"):
            if item.lower() == _get_grocery_item_name(grocery_item):
                return grocery_item

    return None

def _get_grocery_item_name(item):
    orig_name = item.get("name")
    return orig_name[:orig_name.index("(")].strip().lower()

def _get_grocery_item_amount(item):
    match = re.search(r"\((?P<amount>.+)\)", item.get("name"))
    if match:
        return match.group("amount")
    else:
        return ""

def _update_item_amount(item, amount):
    if item.get("state") == CHECKED_STATE or re.match(r".+ \(\)", item.get("name")):
        item["name"] = " ".join([_get_grocery_item_name(item), "({})".format(amount)])
    else:
        if amount:
            item["name"] = re.sub(r"\)", " + {})".format(amount), item.get("name"))

def _get_grocery_list():
    try:
        return requests.get("https://api.trello.com/1/cards/{}/checklists".format(_GROCERY_LIST_ID), auth=_get_auth()).json()
    except:
        return {}

def _get_grocery_items_for_day(day):
    trello_id = _DAY_LIST_MAP[day]
    day_recipes = requests.get("https://api.trello.com/1/lists/{}/cards".format(trello_id), auth=_get_auth()).json()
    for day_recipe in day_recipes:
        for ingredient_list_ids in day_recipe['idChecklists']:
            return requests.get("https://api.trello.com/1/checklists/{}/checkitems".format(ingredient_list_ids), auth=_get_auth()).json() 
    else:
        return []

def _get_auth():
    global _AUTH

    if _AUTH is None:
        _AUTH = _load_auth()

    return _AUTH

def _save_item(item):
    params = {}
    params["name"] = item["name"]
    params["state"] = item["state"]
    params["idChecklist"] = item["idChecklist"]
    requests.request("PUT", "https://api.trello.com/1/cards/{}/checkItem/{}".format(_GROCERY_LIST_ID, item.get("id")), params=params, auth=_get_auth())