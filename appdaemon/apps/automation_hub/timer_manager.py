import datetime
import threading

import api_handle
from util import logger

INFINITE_REPEATS = -1
timer_map = {}
map_lock = threading.RLock()

def schedule_oneoff_task(name, callback, start):
    if api_handle.instance:
        logger.info(f"Scheduling oneoff callback: {name}")
        api_handle.instance.run_once(api_handle.instance.scheduler_callback, start, partial=callback, title=name)

def schedule_polling_task(name, callback, interval):
    if api_handle.instance:
        logger.info(f"Scheduling polling callback: {name}")
        api_handle.instance.run_every(api_handle.instance.scheduler_callback, "now", interval, partial=callback, title=name)

def schedule_daily_task(name, callback, start):
    if api_handle.instance:
        logger.info(f"Scheduling daily callback: {name}")
        api_handle.instance.run_daily(api_handle.instance.scheduler_callback, start, partial=callback, title=name)
    else:
        logger.error("API Handle is None")
    
def start_repeat_timer(name, callback, repeat_seconds, start=datetime.datetime.now(), num_repeats=INFINITE_REPEATS):
    if api_handle.instance:
        with map_lock:
            if name not in timer_map:
                logger.info("Scheduling callback in {} seconds".format(repeat_seconds))
                timer = api_handle.instance.run_every(api_handle.instance.timer_callback, start, repeat_seconds, title=name, partial=callback)
                timer_map[name] = timer
                return True
            else:
                logger.warning("Timer {} is already in map, not starting".format(name))
    else:
        logger.error("API Handle is None")
        
    return False

def start_timer(name, callback, replace=True, seconds=0, minutes=0, hours=0, days=0):
    delta = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
    if api_handle.instance:
        with map_lock:
            if name not in timer_map:
                logger.info("Scheduling callback of {} in {} seconds".format(name, delta.total_seconds()))
                timer = api_handle.instance.run_in(api_handle.instance.timer_callback, int(delta.total_seconds()), title=name, partial=callback)
                timer_map[name] = timer
                return True
            elif replace:
                logger.info("Scheduling replacement callback of {} in {} seconds".format(name, delta.total_seconds()))
                cancel_timer(name)
                timer = api_handle.instance.run_in(api_handle.instance.timer_callback, int(delta.total_seconds()), title=name, partial=callback)
                timer_map[name] = timer
                return True
            else:
                logger.warning("Timer {} is already in map, not starting".format(name))
    else:
        logger.error("API Handle is None")
        
    return False

def cancel_timer(name):
    if api_handle.instance:
        with map_lock:
            if name in timer_map:
                api_handle.instance.cancel_timer(timer_map[name])
                del timer_map[name]
            else:
                logger.warning("Timer {} is not in map".format(name))
    else:
        logger.error("API Handle is None")
            
            
def remove_timer(name):
    global timer_map
    
    with map_lock:
        if name in timer_map:
            del timer_map[name]