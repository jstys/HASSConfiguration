import functools

import timer_manager
from scheduled_tasks.daily import jim_wfh_check

API_HANDLE = None

def set_api_handle(handle):
    global API_HANDLE
    API_HANDLE = handle

def schedule_daily_tasks():
    timer_manager.schedule_daily_task("jim_wfh_check", functools.partial(jim_wfh_check.callback, API_HANDLE), jim_wfh_check.START_TIME)