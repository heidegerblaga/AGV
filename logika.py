import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math

""" 
###  Założenia  :
1. Wózek stoi mniej więcej  frontem  do ściany  (ściana d1 "x"- wózek - ściana d2 d3 "y  ~ 90st)
2. Wózek stoi w odległości około 2 metrów (można poeksperymentować na dalszą odległość ale wtedy czujniki zwracają niepoprawne pomiary) 
3. kąt punkt_dokowania - wózek - ściana nie może wynosić więcej niż 45st


### Co trzeba zrobić?

Dopasuj prędkość  agv w taki sposób aby nie skręcał zbyt szybko, 
czujnik może tego nie wyłapać w porę a wtedy zacznie kręcić w kółko.
jeżeli ci się chce możesz dodać reguły które które będą uwzględniać taką sytuacje
wtedy musisz zrobić dodatkowy warunrk np if d3 > d2 ( czyli czujnik odwrócił się do ściany "x" ) tan((d3-d2)/30) 

"""

# Definicja zmiennych wejściowych i wyjściowych
x_distance = ctrl.Antecedent(np.arange(0, 5001, 1), 'x')  # Lewy czujnik
y_distance = ctrl.Antecedent(np.arange(0, 5001, 1), 'y')  # Prawy czujnik
angle = ctrl.Antecedent(np.arange(0, 91, 1), 'angle')
speed_L = ctrl.Consequent(np.arange(150, 256, 1), 'speed_L')  # Prędkość lewego koła
speed_R = ctrl.Consequent(np.arange(150, 256, 1), 'speed_R')  # Prędkość prawego koła

# Funkcje przynależności dla czujników d1 i d2
x_distance['close'] = fuzz.trimf(x_distance.universe, [0, 0, 500])
x_distance['medium'] = fuzz.trimf(x_distance.universe, [500, 1000, 1500])
x_distance['far'] = fuzz.trimf(x_distance.universe, [1500, 2000, 10000])


""" Być może trimf będzie zbyt gwałtowny dla tych czujników, jakby to nie działało to zmień na tramf i 
 listę [500,700,800] zamień na [500,600,700,800] itd chociaż te czujniki są tak chujowe że wątpie by to 
 pomogło xD"""
y_distance['close'] = fuzz.trimf(y_distance.universe, [0, 0, 500])
y_distance['medium'] = fuzz.trimf(y_distance.universe, [500, 700, 800])
y_distance['far'] = fuzz.trimf(y_distance.universe, [1000, 2000, 30000])


""" Jak ci się chcę to możesz określić wektor początkowy względem punktu dokowania 
i potem zamienić to na kąt, i wtedy mozesz zrobić :

    angle[bad] =fuzz.trimf(angle.universe, [-100, 0, 0])
    angle[good] = fuzz.trimf(angle.universe, [wsp.kierunkowy -1 , wsp.kierunkowy, wsp.kierunkowy +1])
    
tylko przy takim czymś musiałbyś to wpakować w klasę, przykładową klasę masz na branchu finnal """
angle['zero'] = fuzz.trimf(angle.universe, [-100, 0, 0])
angle['sharp'] = fuzz.trimf(angle.universe, [10, 15, 30])
angle['q-sharp'] = fuzz.trimf(angle.universe, [15, 30 , 45])
angle['half-sharp'] = fuzz.trimf(angle.universe, [45, 60 , 89])



"""
 I tutaj będzie cała zabawa, zmieniaj przedziały prędkości w taki sposób aby czujniki nadążały 
"""
speed_L['stop'] = fuzz.trimf(speed_L.universe, [255, 255, 255])
speed_L['slow'] = fuzz.trimf(speed_L.universe, [205, 245, 255])
speed_L['medium'] = fuzz.trimf(speed_L.universe, [160, 180, 205])
speed_L['fast'] = fuzz.trimf(speed_L.universe, [150, 160, 180])

speed_R['stop'] = fuzz.trimf(speed_R.universe, [255, 255, 255])
speed_R['slow'] = fuzz.trimf(speed_R.universe, [205, 245, 255])
speed_R['medium'] = fuzz.trimf(speed_R.universe, [160, 180, 205])
speed_R['fast'] = fuzz.trimf(speed_R.universe, [150, 160, 180])

# nakierowanie wózka na punkt dokowania oraz ruszenie w jego kierunku ewentualne korekta przy nadmiernym skręcie
rule1 = ctrl.Rule(x_distance['far'] & y_distance['far'] & angle['zero'] | angle['sharp'] , (speed_L['stop'], speed_R['fast']))
rule2 = ctrl.Rule(x_distance['far'] & y_distance['far'] & angle['q-sharp'], # I tu np możesz wstawić że tylko wtedy kiedny angle[good]
                  (speed_L['medium'], speed_R['medium']))
rule3 = ctrl.Rule(x_distance['far'] & y_distance['far'] & angle['half-sharp'], (speed_L['medium'], speed_R['stop']))

# zbliżenie się do punku dokowania, korygowanie kursu na ścianę
rule5 = ctrl.Rule(~x_distance['far'] & ~y_distance['far']& (angle['sharp']|angle['zero']), (speed_L['medium'], speed_R['slow']))
rule4 = ctrl.Rule(~x_distance['far'] & ~y_distance['far'] , (speed_L['slow'], speed_R['slow']))


rule6 = ctrl.Rule(x_distance['close'] & ~y_distance['close'] & ~angle['half-sharp'], (speed_L['stop'], speed_R['slow']))
rule7 = ctrl.Rule(x_distance['close'] & y_distance['close'] & ~angle['zero'], (speed_L['slow'], speed_R['stop']))
rule8 = ctrl.Rule(x_distance['close'] & y_distance['close'] & (angle['zero']|angle['sharp']), (speed_L['stop'], speed_R['stop']))

''' 
Te reguły powinny zawsze działać przy spełnionych założeniach ale wiadomo teoria jedno 
praktyka drugie
'''


# System kontroli
speed_control_system = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5, rule6,rule7])
speed_simulator = ctrl.ControlSystemSimulation(speed_control_system)

# Funkcja sterowania wózkiem AGV
def control_agv(d1_val, d2_val,d3_val):

    print("jestem")
    degrees = math.degrees(math.tan((d2_val-d3_val)/30))
    cos = math.cos(math.radians(degrees))
    print(f"degrees {degrees}")
    print(f"cos {cos}")
    speed_simulator.input['x'] = d2_val * cos if d2_val-d3_val>0 else d1_val
    print(f"d2 : {d2_val}")
    print(d2_val * cos)
    speed_simulator.input['y'] = d1_val * cos if d2_val-d3_val>0 else d1_val
    print(f"d1 : {d1_val}")
    print(d1_val * cos)
    speed_simulator.input['angle'] = degrees

    speed_simulator.compute()
    return speed_simulator.output['speed_L'], speed_simulator.output['speed_R']

print(control_agv(700,1000,790))

