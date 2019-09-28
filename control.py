## This program will serve as the Controller. It will be called during every event to handle changes in the system
import numpy as np

class simple_controller:
    ## This controller functions as a Bang-Bang or Binary Controller

    def __init__(self):
        self.target = 0.0
        self.error = 0.0
        self.position = 0.0
        self.control_scheme = { 'right' : 0.5236 , 'left' : -0.5236 , 'center' : 0.0}
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
        self.control_scheme = { 'right' : 0.1309 , 'left' : -0.1309 , 'center' : 0.0}
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