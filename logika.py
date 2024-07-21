import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

# Definicja zmiennych wejściowych i wyjściowych
d1 = ctrl.Antecedent(np.arange(0, 5001, 1), 'd1')  # Lewy przedni czujnik
d3 = ctrl.Antecedent(np.arange(0, 5001, 1), 'd3')  # Prawy przedni czujnik
d2 = ctrl.Antecedent(np.arange(0, 5001, 1), 'd2')  # Lewy boczny czujnik
speed_L = ctrl.Consequent(np.arange(0, 256, 1), 'speed_L')  # Prędkość lewego koła
speed_R = ctrl.Consequent(np.arange(0, 256, 1), 'speed_R')  # Prędkość prawego koła

# Funkcje przynależności dla czujników d1, d2 i d3
d1['close'] = fuzz.trimf(d1.universe, [0, 0, 500])
d1['medium'] = fuzz.trimf(d1.universe, [250, 500, 1000])
d1['far'] = fuzz.trimf(d1.universe, [800, 1000, 5000])

d2['close'] = fuzz.trimf(d2.universe, [0, 0, 500])
d2['medium'] = fuzz.trimf(d2.universe, [250, 500, 1000])
d2['far'] = fuzz.trimf(d2.universe, [800, 1000, 5000])

d3['close'] = fuzz.trimf(d3.universe, [0, 0, 500])
d3['medium'] = fuzz.trimf(d3.universe, [250, 500, 1000])
d3['far'] = fuzz.trimf(d3.universe, [800, 1000, 5000])

# Funkcje przynależności dla prędkości lewego i prawego koła
speed_L['stop'] = fuzz.trapmf(speed_L.universe, [245, 255,255, 255])
speed_L['slow'] = fuzz.trapmf(speed_L.universe, [190,200, 245, 255])
speed_L['medium'] = fuzz.trapmf(speed_L.universe, [155,170, 190, 200])
speed_L['fast'] = fuzz.trapmf(speed_L.universe, [0,0, 155, 170])

speed_R['stop'] = fuzz.trapmf(speed_R.universe, [245, 255,255, 255])
speed_R['slow'] = fuzz.trapmf(speed_R.universe, [190,200, 245, 255])
speed_R['medium'] = fuzz.trapmf(speed_R.universe, [155,170,190, 200])
speed_R['fast'] = fuzz.trapmf(speed_R.universe, [0,0, 155, 170])

# Definicja reguł rozmytych
# Reguły dla korygowania kąta wózka
rule1 = ctrl.Rule(d1['close'] & d3['close'], consequent=(speed_L['stop'] % 1, speed_R['stop'] % 1))
rule2 = ctrl.Rule(d1['far'] & d3['far'] , consequent=(speed_L['medium'] % 1, speed_R['medium'] % 1))


# System kontroli
speed_control_system = ctrl.ControlSystem([rule1, rule2])

speed_simulator = ctrl.ControlSystemSimulation(speed_control_system)



# Funkcja sterowania wózkiem AGV
def control_agv(d1_val, d2_val, d3_val):
    speed_simulator.input['d1'] = d1_val
    speed_simulator.input['d2'] = d2_val
    speed_simulator.input['d3'] = d3_val
    speed_simulator.compute()
    return speed_simulator.output['speed_L'], speed_simulator.output['speed_R']

#Rysowanie wykresów funkcji przynależności
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 15))

axes[0, 0].plot(d1.universe, d1['close'].mf, 'b', linewidth=1.5, label='Close')
axes[0, 0].plot(d1.universe, d1['medium'].mf, 'g', linewidth=1.5, label='Medium')
axes[0, 0].plot(d1.universe, d1['far'].mf, 'r', linewidth=1.5, label='Far')
axes[0, 0].set_title('d1 (Left Front Sensor)')
axes[0, 0].legend()

axes[0, 1].plot(d3.universe, d3['close'].mf, 'b', linewidth=1.5, label='Close')
axes[0, 1].plot(d3.universe, d3['medium'].mf, 'g', linewidth=1.5, label='Medium')
axes[0, 1].plot(d3.universe, d3['far'].mf, 'r', linewidth=1.5, label='Far')
axes[0, 1].set_title('d3 (Right Front Sensor)')
axes[0, 1].legend()

axes[1, 0].plot(d2.universe, d2['close'].mf, 'b', linewidth=1.5, label='Close')
axes[1, 0].plot(d2.universe, d2['medium'].mf, 'g', linewidth=1.5, label='Medium')
axes[1, 0].plot(d2.universe, d2['far'].mf, 'r', linewidth=1.5, label='Far')
axes[1, 0].set_title('d2 (Left Side Sensor)')
axes[1, 0].legend()

axes[1, 1].plot(speed_L.universe, speed_L['stop'].mf, 'b', linewidth=1.5, label='Stop')
axes[1, 1].plot(speed_L.universe, speed_L['slow'].mf, 'g', linewidth=1.5, label='Slow')
axes[1, 1].plot(speed_L.universe, speed_L['medium'].mf, 'r', linewidth=1.5, label='Medium')
axes[1, 1].plot(speed_L.universe, speed_L['fast'].mf, 'y', linewidth=1.5, label='Fast')
axes[1, 1].set_title('speed_L (Left Wheel Speed)')
axes[1, 1].legend()

axes[2, 0].plot(speed_R.universe, speed_R['stop'].mf, 'b', linewidth=1.5, label='Stop')
axes[2, 0].plot(speed_R.universe, speed_R['slow'].mf, 'g', linewidth=1.5, label='Slow')
axes[2, 0].plot(speed_R.universe, speed_R['medium'].mf, 'r', linewidth=1.5, label='Medium')
axes[2, 0].plot(speed_R.universe, speed_R['fast'].mf, 'y', linewidth=1.5, label='Fast')
axes[2, 0].set_title('speed_R (Right Wheel Speed)')
axes[2, 0].legend()

fig.tight_layout()
plt.show()
