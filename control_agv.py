# coding: utf-8
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

d1 = ctrl.Antecedent(np.arange(0, 5001, 1), 'd1')  # Lewy przedni czujnik

d3 = ctrl.Antecedent(np.arange(0, 5001, 1), 'd3')  # Prawy przedni czujnik

d2 = ctrl.Antecedent(np.arange(0, 5001, 1), 'd2')  # Lewy boczny czujnik

speed_L = ctrl.Consequent(np.arange(0, 256, 1), 'speed_L')  # Prędkość lewego koła

speed_R = ctrl.Consequent(np.arange(0, 256, 1), 'speed_R')  # Prędkość prawego koła


# Funkcje przynależności dla czujników d1, d2 i d3
d1['close'] = fuzz.trimf(d1.universe, [0, 200, 500])
d1['medium'] = fuzz.trimf(d1.universe, [500, 500, 1000])
d1['far'] = fuzz.trapmf(d1.universe, [800, 1000, 5000,10000])


d2['close'] = fuzz.trimf(d2.universe, [0, 0, 500])
d2['medium'] = fuzz.trimf(d2.universe, [500, 500, 1000])
d2['far'] = fuzz.trapmf(d2.universe, [800, 1000, 5000,10000])


d3['close'] = fuzz.trimf(d3.universe, [0, 0, 500])
d3['medium'] = fuzz.trimf(d3.universe, [500, 500, 1000])
d3['far'] = fuzz.trapmf(d3.universe, [800, 1000, 5000,10000])


# Funkcje przynależności dla prędkości lewego i prawego koła
speed_L['stop'] = fuzz.trimf(speed_L.universe, [255, 255,255])
speed_L['slow'] = fuzz.trapmf(speed_L.universe, [190,200, 245, 255])
speed_L['medium'] = fuzz.trapmf(speed_L.universe, [155,170, 190, 200])
speed_L['fast'] = fuzz.trimf(speed_L.universe, [0, 155, 170])


speed_R['stop'] = fuzz.trimf(speed_R.universe, [255, 255,255])
speed_R['slow'] = fuzz.trapmf(speed_R.universe, [190,200, 245, 255])
speed_R['medium'] = fuzz.trapmf(speed_R.universe, [155,170,190, 200])
speed_R['fast'] = fuzz.trimf(speed_R.universe, [0,155, 170])


# Definicja reguł rozmytych
# Reguły dla korygowania kąta wózka
rule1 = ctrl.Rule(d1['close'] & d2['close'] & d3['close'], consequent=(speed_L['stop'] , speed_R['stop'] ))
rule2 = ctrl.Rule(d1['far'] & d3['far'] , consequent=(speed_L['fast'] , speed_R['fast'] ))
rule3 = ctrl.Rule(d1['medium'] & d3['medium'] , consequent=(speed_L['medium'] , speed_R['medium'] ))
rule4 = ctrl.Rule(d2['medium'] | d2['far'] , consequent=(speed_L['medium'] , speed_R['medium'] ))

# System kontroli
speed_control_system = ctrl.ControlSystem([rule1, rule2,rule3,rule4])

speed_simulator = ctrl.ControlSystemSimulation(speed_control_system)
# Funkcja sterowania wózkiem AGV
def control_agv(d1_val, d2_val, d3_val):
    speed_simulator.input['d1'] = d1_val
    speed_simulator.input['d2'] = d2_val
    speed_simulator.input['d3'] = d3_val
    speed_simulator.compute()
    return speed_simulator.output['speed_L'], speed_simulator.output['speed_R']


dist = [[2000,2000,2000],[1000,1000,1000],[500,500,500],[100,100,100],[10,10,10],[0,0,0]]
i = 1
for l in dist:
    print(i)
    print(control_agv(l[0],l[1],l[2]))
    i += 1
