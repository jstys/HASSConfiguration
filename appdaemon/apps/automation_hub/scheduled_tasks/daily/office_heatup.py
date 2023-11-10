import state_machine
import timer_manager
from util import hassutil
from actions.thermostat_action import ThermostatAction
from actions.light_action import LightAction

START_TIME = "06:00:00"

def _enable_office_heat():
    heat_action = ThermostatAction().add_thermostat("Office Minisplit")
    heat_action.turn_on()
    heat_action.set_temperature("74", "heat")

def callback():
    if not hassutil.is_weekend() and not state_machine.is_enabled("Vacation Mode") and state_machine.is_heating_enabled():
        if state_machine.is_enabled("Jim WFH Calendar"):
            LightAction().add_light("Office Lights").turn_on()
            _enable_office_heat()
        else:
            timer_manager.schedule_oneoff_task("office_heatup", _enable_office_heat, "08:00:00")
