import datetime
import threading

from util import logutil

API_HANDLE = None
INFINITE_REPEATS = -1
timer_map = {}
logger = logutil.get_logger("automation_hub")
map_lock = threading.Lock()

def set_api_handle(handle):
    global API_HANDLE
    API_HANDLE = handle

def schedule_daily_task(name, callback, start):
    if API_HANDLE:
        logger.info(f"Scheduling daily callback: {name}")
        API_HANDLE.run_daily(API_HANDLE.scheduler_callback, start, partial=callback, name=name)
    else:
        logger.error("API Handle is None")
    
def start_repeat_timer(name, callback, repeat_seconds, start=datetime.datetime.now(), num_repeats=INFINITE_REPEATS):
    if API_HANDLE:
        with map_lock:
            if name not in timer_map:
                logger.info("Scheduling callback in {} seconds".format(repeat_seconds))
                timer = API_HANDLE.run_every(API_HANDLE.timer_callback, start, repeat_seconds, title=name, partial=callback)
                timer_map[name] = timer
                return True
            else:
                logger.warning("Timer {} is already in map, not starting".format(name))
    else:
        logger.error("API Handle is None")
        
    return False

def start_timer(name, callback, seconds=0, minutes=0, hours=0, days=0):
    delta = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
    if API_HANDLE:
        with map_lock:
            if name not in timer_map:
                logger.info("Scheduling callback in {} seconds".format(delta.total_seconds()))
                timer = API_HANDLE.run_in(API_HANDLE.timer_callback, int(delta.total_seconds()), title=name, partial=callback)
                timer_map[name] = timer
                return True
            else:
                logger.warning("Timer {} is already in map, not starting".format(name))
    else:
        logger.error("API Handle is None")
        
    return False

def cancel_timer(name):
    if API_HANDLE:
        with map_lock:
            if name in timer_map:
                API_HANDLE.cancel_timer(timer_map[name])
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