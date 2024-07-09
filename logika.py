import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definicja zmiennych wejściowych i wyjściowych
d1 = ctrl.Antecedent(np.arange(0, 5001, 1), 'd1')  # Lewy czujnik
d2 = ctrl.Antecedent(np.arange(0, 5001, 1), 'd2')  # Prawy czujnik
speed_L = ctrl.Consequent(np.arange(0, 256, 1), 'speed_L')  # Prędkość lewego koła
speed_R = ctrl.Consequent(np.arange(0, 256, 1), 'speed_R')  # Prędkość prawego koła

# Funkcje przynależności dla czujników d1 i d2
d1['close'] = fuzz.trimf(d1.universe, [0, 0, 500])
d1['medium'] = fuzz.trimf(d1.universe, [500, 1000, 2000])
d1['far'] = fuzz.trimf(d1.universe, [1000, 2000, 10000])

d2['close'] = fuzz.trimf(d2.universe, [0, 0, 500])
d2['medium'] = fuzz.trimf(d2.universe, [500, 1000, 2000])
d2['far'] = fuzz.trimf(d2.universe, [1000, 2000, 10000])

# Funkcje przynależności dla prędkości lewego i prawego koła
speed_L['stop'] = fuzz.trimf(speed_L.universe, [245, 255, 255])
speed_L['slow'] = fuzz.trimf(speed_L.universe, [205, 245, 255])
speed_L['medium'] = fuzz.trimf(speed_L.universe, [155, 205, 255])
speed_L['fast'] = fuzz.trimf(speed_L.universe, [0, 155, 205])

speed_R['stop'] = fuzz.trimf(speed_R.universe, [245, 255, 255])
speed_R['slow'] = fuzz.trimf(speed_R.universe, [205, 245, 255])
speed_R['medium'] = fuzz.trimf(speed_R.universe, [155, 205, 255])
speed_R['fast'] = fuzz.trimf(speed_R.universe, [0, 155, 205])

# Definicja reguł rozmytych
rule1 = ctrl.Rule(d1['close'] & d2['close'], (speed_L['stop'], speed_R['stop']))
rule2 = ctrl.Rule(d1['close'] & d2['medium'], (speed_L['slow'], speed_R['medium']))
rule3 = ctrl.Rule(d1['close'] & d2['far'], (speed_L['slow'], speed_R['medium']))
rule4 = ctrl.Rule(d1['medium'] & d2['close'], (speed_L['medium'], speed_R['slow']))
rule5 = ctrl.Rule(d1['medium'] & d2['medium'], (speed_L['medium'], speed_R['medium']))
rule6 = ctrl.Rule(d1['medium'] & d2['far'], (speed_L['medium'], speed_R['slow']))
rule7 = ctrl.Rule(d1['far'] & d2['close'], (speed_L['medium'], speed_R['slow']))
rule8 = ctrl.Rule(d1['far'] & d2['medium'], (speed_L['medium'], speed_R['slow']))
rule9 = ctrl.Rule(d1['far'] & d2['far'], (speed_L['medium'], speed_R['medium']))

# System kontroli
speed_control_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
speed_simulator = ctrl.ControlSystemSimulation(speed_control_system)

# Funkcja sterowania wózkiem AGV
def control_agv(d1_val, d2_val):
    speed_simulator.input['d1'] = d1_val
    speed_simulator.input['d2'] = d2_val
    speed_simulator.compute()
    return speed_simulator.output['speed_L'], speed_simulator.output['speed_R']

# Przykład użycia:
output_speed_L, output_speed_R = control_agv(300, 700)
print(f"Speed Left: {output_speed_L}, Speed Right: {output_speed_R}")
