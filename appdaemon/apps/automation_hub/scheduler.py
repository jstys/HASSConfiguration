from automation_hub import timer_manager
from scheduled_tasks.daily import jim_wfh_check

def schedule_daily_tasks():
    timer_manager.schedule_daily_task("jim_wfh_check", jim_wfh_check.callback, jim_wfh_check.START_TIME)