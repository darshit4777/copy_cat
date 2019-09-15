## This program will serve as the Controller. It will be called during every event to handle changes in the system
import numpy as np

class simple_controller:
    ## This controller functions as a Bang-Bang or Binary Controller

    def __init__(self):
        self.target = 0
        self.error = 0
        self.position = 0
        self.control_scheme = { 'right' : -30 , 'left' : 30 , 'center' : 0}
        self.plate_angular_vel_max = 60
        self.plate_angular_vel = 0
    
    def get_input(self,input):
        self.target = np.deg2rad(self.control_scheme.get(input))

    def control_loop(self):
        self.error = self.target - self.position
        if np.abs(self.error) : 
            self.plate_angular_vel = self.plate_angular_vel_max * self.error / np.abs(self.error)
            return self.plate_angular_vel
        
        return self.plate_angular_vel

    def get_observation(self,plate_angle):
        self.position = np.deg2rad(plate_angle)

        

