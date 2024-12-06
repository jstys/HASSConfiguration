import event_dispatcher
import state_machine
import timer_manager
from util import logger
from scheduled_tasks.daily import vacation_day_heat, vacation_night_heat
from events.input_event import InputEvent
from actions.light_action import LightAction
from actions.thermostat_action import ThermostatAction
from actions.switch_action import SwitchAction

def event_filter(event):
    return event.name == "Vacation Mode"

def register_callbacks():
    event_dispatcher.register_callback(on_state_changed, InputEvent.__name__, event_filter=event_filter)
    
def on_state_changed(event):
    if event.new == "off":
        on_disabled(event)
    elif event.new == "on":
        on_enabled(event)
    else:
        logger.warning("Invalid state transition for vacation mode")

def on_enabled(event):
    if state_machine.is_heating_enabled():
        ThermostatAction().add_thermostat("Oil Thermostat").set_temperature(state_machine.get_number("Vacation Heat"), "heat")
        timer_manager.schedule_daily_task("vacation_day_heat", vacation_day_heat.callback, vacation_day_heat.START_TIME)
        timer_manager.schedule_daily_task("vacation_night_heat", vacation_night_heat.callback, vacation_night_heat.START_TIME)

    if state_machine.is_enabled("Christmas Lights Mode"):
        LightAction().add_light("Christmas Tree Lights").turn_off()
        SwitchAction().add_switches([
            "Smart Strip Outlet 1",
            "Smart Strip Outlet 2",
            "Smart Strip Outlet 3",
            "Smart Strip Outlet 4"
        ]).turn_off()

def on_disabled(event):
    timer_manager.cancel_timer("vacation_day_heat")
    timer_manager.cancel_timer("vacation_night_heat")

    if state_machine.is_heating_enabled():
        ThermostatAction().add_thermostat("Oil Thermostat").set_temperature(state_machine.get_number("Normal Heat"), "heat")