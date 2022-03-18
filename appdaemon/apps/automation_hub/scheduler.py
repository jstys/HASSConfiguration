import timer_manager
from util import hassutil
from scheduled_tasks.daily import office_heatup
from scheduled_tasks.daily import auto_end_sleep_mode

def is_weekend():
    return hassutil.get_current_date().weekday() > 4

def schedule_daily_tasks():
    timer_manager.schedule_daily_task("office_heatup", office_heatup.callback, office_heatup.START_TIME)
    timer_manager.schedule_daily_task("auto_end_sleep_mode", auto_end_sleep_mode.callback, auto_end_sleep_mode.get_starttime(is_weekend()))

def schedule_polling_tasks():
    pass