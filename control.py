## This program will serve as the Controller. It will be called during every event to handle changes in the system
import numpy as np
from sharinGan import DataAnalyser
import time

class simple_controller:
    ## This controller functions as a Bang-Bang or Binary Controller

    def __init__(self):
        self.target = 0.0
        self.error = 0.0
        self.position = 0.0
        self.control_scheme = { 'right' : 0.1309 , 'left' : -0.1309 , 'center' : 0.0}
        self.plate_angular_vel_max = 10*0.174533 # Unit is rad/s 1 degree = 0.0174533 rad
        self.plate_angular_vel = 0
    
    def get_input(self,input):
        self.target = self.control_scheme.get(input)

    def control_loop(self):
        self.error = self.target - self.position
        #print(self.error)

        if np.abs(self.error) : 
            self.plate_angular_vel = self.plate_angular_vel_max * self.error / np.abs(self.error)
            return self.plate_angular_vel
        
        return self.plate_angular_vel

    def get_observation(self,plate_angle):
        self.position = plate_angle
        #print(plate_angle)

    def restart(self):
        ## Resetting Controller Variables
        self.target = 0.0
        self.error = 0.0
        self.position = 0.0

        ## Resetting Control Input
        self.plate_angular_vel = 0

        
class pid_controller:
    def __init__(self):
        self.target = 0.0
        self.error = 0.0
        self.position = 0.0
        self.control_scheme = { 'right' : -0.1309 , 'left' : 0.1309 , 'center' : 0.0}
        self.plate_angular_vel_max = 20*0.174533 # Unit is rad/s 1 degree = 0.0174533 rad
        self.plate_angular_vel = 0
        self.error_prev = 0
        self.P = 10
        self.D = 0.1
        self.I = 0.1
        self.error_integ = 0
        self.dt = 1/30
        

    def get_input(self,input):
        self.target = self.control_scheme.get(input)

    def set_target(self,input_value):
        self.target = input_value


    def control_loop(self):
        self.error = self.target - self.position
        
        #print(self.error)

        
        self.plate_angular_vel = self.P * self.error + self.D * (self.error - self.error_prev) / self.dt + self.I * (self.error_integ)

        self.plate_angular_vel = np.maximum(self.plate_angular_vel, -self.plate_angular_vel_max)
        self.plate_angular_vel = np.minimum(self.plate_angular_vel, self.plate_angular_vel_max)

        self.error_integ = self.error * self.dt + self.error_integ
        self.error_prev = self.error
        #print(self.plate_angular_vel)
        return self.plate_angular_vel

    def get_observation(self,plate_angle):
        self.position = plate_angle
        #print(plate_angle)

    def restart(self):
        ## Resetting Controller Variables
        self.target = 0.0
        self.error = 0.0
        self.position = 0.0
        self.error_prev = 0
        self.error_integ = 0

        ## Resetting Control Input
        self.plate_angular_vel = 0

class ml_controller:
    
    def __init__(self):
        # The ML controller will use available data to generate a model and then it will supply inputs to a PID object
        self.data_analyser = DataAnalyser()
        
        # Generate a dataframe from available data 
        self.data_analyser.genDataFrame()

        
        if self.data_analyser.data_available is True:
            # Normalise dataframe
            self.data_analyser.normDataFrame()

            # Generate Model
            self.data_analyser.copyCatJutsu()

        # Model Variables
        self.plate_angle = 0
        self.position = 804
        self.velocity = 0

        # Input to Controller
        self.control_input = 0

        # Controller time constraints
        self.control_time = 0
        self.control_time_interval = 0.0

    def gen_input(self,position,angle,velocity):
        self.position = position - 804
        #print(self.position)
        self.velocity = velocity
        self.plate_angle = angle
        Y = self.data_analyser.sharin_gan.predict([[self.position,self.plate_angle,self.velocity]])[0]
        #print(Y)
        input_value = Y[0]
        time_interval = Y[1]
        #print(input_value[0])

        # Setting the input value into the range
        current_time = time.time()
        if ((current_time - self.control_time) > self.control_time_interval): 
            self.control_input = input_value * 0.1309 / np.abs(input_value)
            #self.control_time = input_value[0] * 0.1309
            self.control_time = time.time()
            self.control_time_interval = time_interval






