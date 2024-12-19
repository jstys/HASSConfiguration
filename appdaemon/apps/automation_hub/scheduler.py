import timer_manager
from scheduled_tasks.daily import office_heatup
from scheduled_tasks.daily import auto_end_sleep_mode

def schedule_daily_tasks():
    timer_manager.schedule_daily_task("office_heatup_check", office_heatup.callback, office_heatup.START_TIME)
    timer_manager.schedule_daily_task("auto_end_sleep_mode_check", auto_end_sleep_mode.callback, auto_end_sleep_mode.START_TIME)

def schedule_polling_tasks():
    pass