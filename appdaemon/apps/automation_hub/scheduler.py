import timer_manager
from scheduled_tasks.daily import jim_wfh_check
from scheduled_tasks.polling import blue_mtn_poll

def schedule_daily_tasks():
    timer_manager.schedule_daily_task("jim_wfh_check", jim_wfh_check.callback, jim_wfh_check.START_TIME)

def schedule_polling_tasks():
    if blue_mtn_poll.ENABLED:
        timer_manager.schedule_polling_task("blue_mtn_check", blue_mtn_poll.callback, blue_mtn_poll.INTERVAL)