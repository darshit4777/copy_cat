## This program will serve as the Controller. It will be called during every event to handle changes in the system
import numpy as np

class simple_controller:
    ## This controller functions as a Bang-Bang or Binary Controller

    def __init__(self):
        self.target = 0.0
        self.error = 0.0
        self.position = 0.0
        self.control_scheme = { 'right' : 0.5236 , 'left' : -0.5236 , 'center' : 0.0}
        self.plate_angular_vel_max = 0.174533 # Unit is rad/s 1 degree = 0.0174533 rad
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

        

