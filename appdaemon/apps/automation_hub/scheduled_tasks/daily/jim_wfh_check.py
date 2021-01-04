import state_machine
from actions.thermostat_action import ThermostatAction
from actions.light_action import LightAction

START_TIME = "07:00:00"

def callback(api_handle):
    if state_machine.is_enabled("jim_wfh_calendar"):

        LightAction().add_light("office_lights").turn_on()

        if state_machine.is_heating_enabled():
            heat_action = ThermostatAction().add_thermostat("office_heat")
            heat_action.set_temperature("74", "heat")
