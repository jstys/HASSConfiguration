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
    "Monday": "",
    "Tuesday": "",
    "Wednesday": "",
    "Thursday": "",
    "Friday": "",
    "Saturday": ""
}
_GROCERY_LIST_ID = "1iKTzp7F"

def generate_grocery_list_from_meal_plan():
    pass

def add_to_grocery_list(item_name, amount=""):
    item = _get_item_reference_from_grocery_list(item_name, _get_grocery_list())
    if item:
        _update_item_amount(item, amount)
        item["state"] = UNCHECKED_STATE
        _save_item(item)
        return True, " ".join([item, "added to the grocery list"])
    else:
        return False, " ".join([item, "is not on the grocery list"])

def remove_from_grocery_list(item_name):
    item = _get_item_reference_from_grocery_list(item_name, _get_grocery_list())
    if item:
        _update_item_amount(item, "")
        item["state"] = CHECKED_STATE
        _save_item(item)
        return True, " ".join([item, "removed from the grocery list"])
    else:
        return False, " ".join([item, "is not on the grocery list"])

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
    return re.sub(r"\(.*\)", "", item.get("name")).strip().lower()

def _update_item_amount(item, amount):
    if item.get("state") == CHECKED_STATE or re.match(r".+ \(\)", item.get("name")):
        item["name"] = " ".join([_get_grocery_item_name(item), "({})".format(amount)])
    else:
        item["name"] = re.sub(r"\)", " + {})".format(amount), item.get("name"))

def _get_grocery_list():
    try:
        return requests.get("https://api.trello.com/1/cards/{}/checklists".format(_GROCERY_LIST_ID), auth=_get_auth()).json()
    except:
        return {}

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