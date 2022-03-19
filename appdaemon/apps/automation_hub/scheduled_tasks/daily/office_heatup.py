import state_machine
import timer_manager
from actions.thermostat_action import ThermostatAction
from actions.light_action import LightAction

START_TIME = "06:00:00"

def _enable_office_heat():
    heat_action = ThermostatAction().add_thermostat("office_heat")
    heat_action.turn_on()
    heat_action.set_temperature("74", "heat")

def callback():
    if state_machine.is_heating_enabled():
        if state_machine.is_enabled("jim_wfh_calendar"):
            LightAction().add_light("office_lights").turn_on()
            if state_machine.is_heating_enabled():
                _enable_office_heat()
        else:
            timer_manager.schedule_oneoff_task("office_heatup", _enable_office_heat, "08:00:00")
