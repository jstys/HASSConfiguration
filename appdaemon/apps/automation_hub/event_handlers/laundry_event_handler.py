import event_dispatcher
import timer_manager
import state_machine
from util import logger
from util import hassutil
from events.power_sensor_off_event import PowerSensorOffEvent
from events.power_sensor_on_event import PowerSensorOnEvent
from actions.discord_notify_action import DiscordNotifyAction
from actions.tts_action import TTSAction

WASHER_IDLE_MINUTES = 2
DRYER_MIN_RUNTIME_MINUTES = 5

dryer_start = None
washer_start = None

def washer_filter(event):
    return event.name == "Washer Running Sensor"
    
def dryer_filter(event):
    return event.name == "Dryer Running Sensor"

def register_callbacks():
    event_dispatcher.register_callback(on_washer_on_event, PowerSensorOnEvent.__name__, event_filter=washer_filter)
    event_dispatcher.register_callback(on_washer_off_event, PowerSensorOffEvent.__name__, event_filter=washer_filter)
    event_dispatcher.register_callback(on_dryer_on_event, PowerSensorOnEvent.__name__, event_filter=dryer_filter)
    event_dispatcher.register_callback(on_dryer_off_event, PowerSensorOffEvent.__name__, event_filter=dryer_filter)
    
def on_washer_on_event(event):
    global washer_start

    logger.info("Washer turned on")
    timer_manager.cancel_timer("laundry_washer_timer")

    washer_start = hassutil.get_current_datetime()

def on_washer_off_event(event):
    logger.info("Washer turned off")
    
    if washer_start is not None:
        timer_manager.start_timer("laundry_washer_timer", on_washer_finished, minutes=WASHER_IDLE_MINUTES)

def on_washer_finished():
    global washer_start
    DiscordNotifyAction().set_message("Washing Machine has finished").add_channel("general").notify()

    if not state_machine.is_enabled("Sleep Mode"):
        TTSAction().add_assistants(["Living Room MPD", "Master Bedroom MPD"]).say("Washer has finished")

    washer_start = None

def on_dryer_on_event(event):
    global dryer_start

    logger.info("Dryer turned on")
    dryer_start = hassutil.get_current_datetime()

def on_dryer_off_event(event):
    logger.info("Dryer turned off")

    if dryer_start is not None:
        curtime = hassutil.get_current_datetime()
        runtime = curtime - dryer_start
        runtime_minutes = int(runtime.total_seconds() / 60)
        if runtime_minutes > DRYER_MIN_RUNTIME_MINUTES:
            logger.info("Dryer has run for at least 5 minutes")
            _notify_dryer_finish()
        else:
            logger.info("False alarm, dryer ran less than 5 minutes")

def _notify_dryer_finish():
    global dryer_start

    if not state_machine.is_enabled("Sleep Mode"):
        TTSAction().add_assistants(["Living Room MPD", "Master Bedroom MPD"]).say("Dryer has finished")
        
    DiscordNotifyAction().set_message("Dryer has finished").add_channel("general").notify()
    dryer_start = None
