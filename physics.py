# This program will serve as the physics engine for a 2D Ball - Plate system. 
# The physics is quite simple, second order kinetic models for rotational motion of a plate
# and rolling motion of a ball down a plate
import numpy as np
import time
class ball_plate_system:
    def __init__(self,ball_radius = 0.025, plate_radius = 0.3 , mu = 0.2, ball_init_x = 804, ball_init_y = 515):
        ## Defining System Dimensions
        self.ball_radius = ball_radius
        self.plate_radius = plate_radius

        ## Defining Ball Parameters
        self.ball_pos_x = ball_init_x
        self.ball_pos_y = ball_init_y
        self.ball_vel_x = 0
        self.ball_vel_y = 0
        self.ball_acc = 0
    
        self.ball_init_x = ball_init_x    # The init values will remain constant throughout program execution
        self.ball_init_y = ball_init_y

        ## Time parameters
        self.time_delay = 0
        self.previous_time = 0

        ## Defining Plate Parameters
        self.plate_angle = 0
        self.plate_angular_vel = 0
        

        ## Defining Physical Constants
        self.mu = mu   ## Ball - Plate rolling friction
        self.g = 9.81   ## Acceleration due to gravity 
        self.dt = 1/30

    def get_input(self,thetadot):
        self.plate_angular_vel = thetadot

    def update(self):
        current_time = time.clock()
        self.time_delay = current_time - self.previous_time
        #print(self.time_delay)
        self.previous_time = current_time
        
        ## Updating the Plate Params using simple rotational physics
        self.plate_angle = self.plate_angle + self.plate_angular_vel * self.dt
        #print(self.plate_angle)
        
        ## Updating Ball Params using Rolling Ball Model
        if self.ball_vel_x != 0 :
            if self.ball_vel_x > 0 :
                self.ball_acc = self.g * np.sin(self.plate_angle) - self.mu * self.g * np.cos(self.plate_angle)
            else :
                self.ball_acc = self.g * np.sin(self.plate_angle) + self.mu * self.g * np.cos(self.plate_angle)

            #print(self.ball_acc)
        else :
            self.ball_acc = self.g * np.sin(self.plate_angle)

        self.ball_vel_x = self.ball_vel_x + self.ball_acc * np.cos(self.plate_angle) * self.dt
        
        self.ball_pos_x = self.ball_pos_x + self.ball_vel_x * self.dt
        #print(self.ball_pos_x)

        ## Adjusting Ball Position Y so that it is always on the plate 
        self.ball_pos_y = self.ball_init_y + np.tan(self.plate_angle) * ( self.ball_pos_x - self.ball_init_x)


        #print(self.plate_angle)
        #print(self.plate_angular_vel)
    
    def restart(self):
        ## Reset Ball Parameters
        self.ball_pos_x = self.ball_init_x
        self.ball_pos_y = self.ball_init_y
        self.ball_vel_x = 0
        self.ball_vel_y = 0
        self.ball_acc = 0

        ## Reset Time parameters
        self.time_delay = 0
        self.previous_time = 0

        ## Reset Plate parameters
        self.plate_angle = 0
        self.plate_angular_vel = 0



