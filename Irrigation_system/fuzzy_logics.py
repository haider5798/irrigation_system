import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def calculate_timing(temp_value, humidity_value, moisture_value):
    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    temp = ctrl.Antecedent(np.arange(0, 50, 1), 'temp')
    humidity = ctrl.Antecedent(np.arange(0, 50, 1), 'humidity')
    soil_moisture = ctrl.Antecedent(np.arange(0, 50, 1), 'soil_moisture')
    time = ctrl.Consequent(np.arange(0, 60, 1), 'time')

    temp.automf(5)
    humidity.automf(5)
    soil_moisture.automf(5)

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    time[15] = fuzz.trimf(time.universe, [0, 0, 15])
    time[30] = fuzz.trimf(time.universe, [0, 15, 30])
    time[45] = fuzz.trimf(time.universe, [15, 30, 45])
    rule1 = ctrl.Rule(temp['poor'] | humidity['poor'] | soil_moisture['average'], time[15])
    rule2 = ctrl.Rule(humidity['average'] | temp['average'] | soil_moisture['poor'], time[30])
    rule3 = ctrl.Rule(humidity['good'] | temp['good'] | soil_moisture['poor'], time[45])

    timing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    timing = ctrl.ControlSystemSimulation(timing_ctrl)

    # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
    # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
    timing.input['temp'] = temp_value
    timing.input['humidity'] = humidity_value
    timing.input['soil_moisture'] = moisture_value

    timing.compute()
    return timing.output['time']


