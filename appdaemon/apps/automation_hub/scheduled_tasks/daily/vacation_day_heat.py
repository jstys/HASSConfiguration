import state_machine
from actions.thermostat_action import ThermostatAction

START_TIME = "08:00:00"

def callback():
    if state_machine.is_enabled("Vacation Mode") and state_machine.is_heating_enabled():
        ThermostatAction().add_thermostat("Oil Thermostat").set_temperature(state_machine.get_number("Vacation Heat"), "heat")
