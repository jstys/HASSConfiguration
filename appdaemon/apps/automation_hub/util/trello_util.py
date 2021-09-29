import re

import requests
from requests.models import HTTPError
from requests_oauthlib import OAuth1
from backoff import expo, on_exception

API_BASE = "https://api.trello.com/1"
CHECKED_STATE = "complete"
UNCHECKED_STATE = "incomplete"

_AUTH = None
_GROCERY_LIST_ID = "1iKTzp7F"
_MEALPLAN_BOARD_ID = "BYUf1NJ0"

session = None

def set_auth(key, secret, oauth):
    global _AUTH
    
    _AUTH = OAuth1(key, secret, oauth)

def archive_last_week():
    global session

    if session is not None:
        return False, []

    session = requests.Session()

    day_list_map = _get_day_lists()
    recent_list = _get_recent_list()
    if recent_list:
        for _, list_id in day_list_map.items():
            trello_id = list_id
            day_recipes = requests.get("{}/lists/{}/cards".format(API_BASE, trello_id), auth=_get_auth()).json()
            for day_recipe in day_recipes:
                requests.put("{}/cards/{}/idList?value={}".format(API_BASE, day_recipe['id'], recent_list), auth=_get_auth())

    session.close()
    session = None

def clear_grocery_list():
    global session

    if session is not None:
        return False, []

    session = requests.Session()

    _clear_all()

    session.close()
    session = None

def generate_grocery_list_from_meal_plan():
    global session

    if session is not None:
        return False, []

    session = requests.Session()
    failed_to_add = []

    cache = _create_grocery_cache()
    _reset_all_item_amounts(cache)

    day_list_map = _get_day_lists()

    for day, _ in day_list_map.items():
        for item in _get_grocery_items_for_day(day, day_list_map):
            name = _get_grocery_item_name(item)
            amount = _get_grocery_item_amount(item)
            result, _ = _add_to_grocery_list(name, cache, amount=amount)
            if not result:
                failed_to_add.append("{} ({}) - {}".format(name, amount, day))

    for name, item in cache.items():
        item["pos"] = "bottom"
        _save_item(item)

    session.close()
    session = None
    if failed_to_add:
        return False, failed_to_add
    else:
        return True, []

def _clear_all():
    cache = _create_grocery_cache()
    for _, item in cache.items():
        item["state"] = CHECKED_STATE

    _reset_all_item_amounts(cache)

    for _, item in cache.items():
        item["pos"] = "bottom"
        _save_item(item)

def _create_grocery_cache():
    grocery_cache = {}
    grocery_json = _get_grocery_list()

    for category in grocery_json:
        category_items = category.get("checkItems")
        sorted_items = sorted(category_items, key=lambda it: it["name"])
        for i, item in enumerate(category_items):
            new_item = item.copy()
            new_item["name"] = sorted_items[i]["name"]
            new_item["state"] = sorted_items[i]["state"]
            grocery_cache[_get_grocery_item_name(new_item)] = new_item

    return grocery_cache

def _add_to_grocery_list(item_name, cache, amount=""):
    item = _get_item_reference_from_grocery_list(item_name, cache)
    if item:
        _update_item_amount(item, amount)
        item["state"] = UNCHECKED_STATE
        return True, " ".join([item_name, "added to the grocery list"])
    else:
        return False, " ".join([item_name, "is not on the grocery list"])

def _reset_all_item_amounts(cache):
    for _, grocery_item in cache.items():
        if grocery_item.get("state") == CHECKED_STATE:
            _update_item_amount(grocery_item, "")

def _get_item_reference_from_grocery_list(item, grocery_cache):
    if item.lower() in grocery_cache:
        return grocery_cache[item.lower()]

    return None

def _get_grocery_item_name(item):
    orig_name = item.get("name")
    if "(" in orig_name:
        return orig_name[:orig_name.index("(")].strip().lower()
    else:
        return orig_name.strip().lower()

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
        return _api_call("GET", "{}/cards/{}/checklists".format(API_BASE, _GROCERY_LIST_ID), auth=_get_auth()).json()
    except Exception as e:
        print(f"Error getting grocery list: {e}")
        return {}

def _get_grocery_items_for_day(day, daymap):
    ingredients = []
    trello_id = daymap[day]
    day_recipes = _api_call("GET", "{}/lists/{}/cards".format(API_BASE, trello_id), auth=_get_auth()).json()
    for day_recipe in day_recipes:
        for ingredient_list_ids in day_recipe['idChecklists']:
            ingredients.extend(_api_call("GET", "{}/checklists/{}/checkitems".format(API_BASE, ingredient_list_ids), auth=_get_auth()).json())

    return ingredients

def _get_auth():
    return _AUTH

def _save_item(item):
    params = {}
    params["name"] = item["name"]
    params["state"] = item["state"]
    params["idChecklist"] = item["idChecklist"]
    if "pos" in item:
        params["pos"] = item["pos"]
    res = _api_call("PUT", "{}/cards/{}/checkItem/{}".format(API_BASE, _GROCERY_LIST_ID, item.get("id")), params=params, auth=_get_auth())

# def _delete_item(item):
#     requests.request("DELETE", "{}/cards/{}/checkItem/{}".format(API_BASE, _GROCERY_LIST_ID, item.get("id")), auth=_get_auth())
    
# def _add_item(checklist, item):
#     params = {}
#     params["name"] = item["name"]
#     params["pos"] = "bottom"
#     params["checked"] = "true" if (item.get("state", "complete") == CHECKED_STATE) else "false"
#     res = requests.post("{}/checklists/{}/checkItems".format(API_BASE, checklist.get("id"), params=params, auth=_get_auth()))

def _get_lists():
    try:
        return _api_call("GET", "{}/boards/{}/lists".format(API_BASE, _MEALPLAN_BOARD_ID), auth=_get_auth()).json()
    except Exception as e:
        print(f"Error getting lists: {e}")
        return []

def _get_day_lists():
    daymap = {}
    for trellolist in _get_lists():
        name = trellolist.get("name")
        listid = trellolist.get("id")
        if name.lower() in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            daymap[name] = listid
    return daymap

def _get_recent_list():
    lists = _get_lists()
    for list in lists:
        name = list.get("name")
        listid = list.get("id")
        if name.lower() == "last week":
            return listid
    
    return None

@on_exception(expo, HTTPError, max_tries=8)
def _api_call(method: str, *args, **kwargs):
    response = session.request(method, *args, **kwargs, timeout=5)
    try:
        response.raise_for_status()
    except HTTPError as e:
        print(f"API Call exception: {e}")
        raise e
    return response