import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
import  math

class  Controller:

    d1 = None
    d2 = None
    d3 = None

    dokX = None
    dokY = None

    destination_degrees = None

    distanceX = None
    distanceY = None
    destination_distance = None



    angle = ctrl.Antecedent(np.arange(0, 91, 1), 'angle')
    destination = ctrl.Antecedent(np.arange(0,5000, 1), 'destination')

    speed_L = ctrl.Consequent(np.arange(0, 256, 1), 'speed_L')
    speed_R = ctrl.Consequent(np.arange(0, 256, 1), 'speed_R')

    speed_L['stop'] = fuzz.trimf(speed_L.universe, [255, 255, 255])
    speed_L['slow'] = fuzz.trapmf(speed_L.universe, [190, 200, 220, 240])
    speed_L['medium'] = fuzz.trapmf(speed_L.universe, [155, 170, 190, 220])
    speed_L['fast'] = fuzz.trapmf(speed_L.universe, [0, 0, 155, 170])

    speed_R['stop'] = fuzz.trimf(speed_R.universe, [255, 255, 255])
    speed_R['slow'] = fuzz.trapmf(speed_R.universe, [190, 200, 220, 240])
    speed_R['medium'] = fuzz.trapmf(speed_R.universe, [155, 170, 190, 220])
    speed_R['fast'] = fuzz.trapmf(speed_R.universe, [0, 0, 155, 170])

    speed_simulator = None

    def __init__(self,d1_val, d2_val, d3_val,dokX,dokY):

        self.dokX = dokX
        self.dokY = dokY
        self.d1 = d1_val
        self.d2 = d2_val
        self.d3 = d3_val

        if abs(d1_val-d2_val) >= 100 :
         #funkcja do wyrównania wózka
         pass
        else :
            pass

        self.distanceX = d1_val - dokX
        self.distanceY = d2_val - dokY
        self.destination_distance = math.sqrt(math.pow(self.distanceX,2) + math.pow(self.distanceY,2))

        self.destination_degrees = math.degrees(math.sin(self.distanceX/self.destination_distance))

        self.angle['far'] = fuzz.trimf(self.angle.universe, [self.destination_degrees + 1, 90, 90 + self.destination_degrees])
        self.angle['good'] = fuzz.trimf(self.angle.universe, [self.destination_degrees, self.destination_degrees, self.destination_degrees])


        self.destination['close'] = fuzz.trimf(self.destination.universe,
                                          [self.destination_distance - 1, self.destination_distance, self.destination_distance])
        self.destination['medium'] = fuzz.trimf(self.destination.universe,
                                           [self.destination_distance + 250, self.destination_distance + 500,
                                            self.destination_distance + 1000])
        self.destination['far'] = fuzz.trimf(self.destination.universe, [self.destination_distance + 800, self.destination_distance + 1000,
                                                               self.destination_distance + 5000])

        rule1 = ctrl.Rule(self.angle['good'] & self.angle['good'],consequent=(self.speed_L['medium'], (self.speed_R['medium'])))

        rule2 = ctrl.Rule(self.destination['far'] & self.destination['far'],consequent=((self.speed_L['medium'], (self.speed_R['medium']))))

        speed_control_system = ctrl.ControlSystem([rule1, rule2])

        self.speed_simulator = ctrl.ControlSystemSimulation(speed_control_system)

    def control_agv(self,d1_val, d2_val, d3_val):
            self.speed_simulator.input['d1'] = d1_val
            self.speed_simulator.input['d2'] = d2_val
            self.speed_simulator.input['d3'] = d3_val
            self.speed_simulator.compute()
            return self.speed_simulator.output['speed_L'], self.speed_simulator.output['speed_R']

    #Rysowanie wykresów funkcji przynależności
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 15))


