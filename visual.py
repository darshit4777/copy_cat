## This file will serve as a standard simulation visualisation module 


## Imports
import pygame
import sys
import time
from physics import ball_plate_system
from control import *
import numpy as np
from sharinGan import DataLogger
from os import system
# Member Functions

def draw_background(screen,background_color):
    # Simply fill the screen with the background color
    screen.fill(background_color)
    pygame.display.update()

def rotate_image(image,angle,image_center):
    # Standard stackoverflow answer to how to rotate an image in pygame
    rotated_image = pygame.transform.rotate(image,angle)
    new_rect = rotated_image.get_rect(center = image_center)

    return rotated_image , new_rect

# TODO : Use a dictionary for position, velocity and acceleration.


class Terminator:
    def __init__(self, physics,control,plate,ball,score):
        self.terminal_condition = False
        self.terminal_condition_timer_active = False
        self.terminal_condition_timestamp = 0
        self.physics = physics
        self.control = control
        self.plate = plate
        self.ball = ball
        self.scoreboard = score
        self.ball_size = 0.0504
        self.ball_center_position_limit_left = - self.ball_size # These limits are expressed in metric
        self.ball_center_position_limit_right =  self.ball_size
        self.ball_limit_position_right = 0.6764 / 2
        self.ball_limit_position_left = -0.6764 / 2
        
        
    

    def check_terminal_condition(self,position):
    
        if (self.ball_center_position_limit_left < position < self.ball_center_position_limit_right): 
            self.terminal_condition = True
            if self.terminal_condition_timer_active:
                
                return
            else :
                self.terminal_condition_timestamp = time.time()
                self.terminal_condition_timer_active = True
                
                return
        else :
            if self.terminal_condition_timer_active :
                self.terminal_condition_timestamp = None
                self.terminal_condition_timer_active = False
                
                return
            else :
                
                return

    
    def check_timer(self):
        if self.terminal_condition_timer_active :
            time_now = time.time()
            if (time_now - self.terminal_condition_timestamp) > 2.0 :
                self.terminal_condition_timer_active = False
                self.terminal_condition_timestamp = None
                self.terminal_condition = False
                self.scoreboard.increase_score()
                self.restart_game()
                return
            else :
                return
        else :
            return

    def restart_game(self):
        ''' This function will restart the game with the Ball at a random location and the Plate at a random angle.
        The random angle of the plate however is always self stabilizing '''

        # Restart the control module 
        self.control.restart()
        
        # Selecting Random Values
        ## Selecting the side where the ball will reappear
        ball_side = np.random.randint(0,2)
        ball_pos_x = np.random.uniform(self.ball_center_position_limit_right,self.ball_limit_position_right - self.ball_size)
        plate_angle_radians = np.random.uniform(0.0900,0.1209)
        #print(plate_angle_radians)

        if ball_side == 0 :
            # Ball appears on the left side 
            ball_pos_x = -ball_pos_x
            plate_angle_radians = -plate_angle_radians

        if ball_side == 1:
            # Ball appears on the right side
            ball_pos_x = ball_pos_x
            plate_angle_radians = plate_angle_radians
            
        # Restarting the Physics module and the Plate Graphics module
        self.physics.restart(ball_pos_x,plate_angle_radians)
        self.plate.restart(plate_angle_radians)

        # After the Physics module x and y values are calculated. We can update the Graphics Engine with the values of the physics engine
        ball_pos_x = self.physics.ball_pos_x
        ball_pos_y = self.physics.ball_pos_y
        self.ball.restart(ball_pos_x,ball_pos_y)
        return
        

    
# Screen Properties
width=1800
height=960

# TODO : Add a scale variable to scale the values of the physics engine with the number of pixels

# Background Properties
## Color
background_color=(0,0,0)

pygame.init()
screen = pygame.display.set_mode((width,height))     ## Inititalising the screen


## Loading Plate
class Plate:
    # TODO : Make the plate position on the screen configurable by Class Declaration
    def __init__(self):
        self.plate = pygame.image.load('Plate.png').convert()
        self.plate_center = (894,625)
        self.plate_rect = (245,600)
        self.plate_angle = 0
        screen.blit(self.plate,self.plate_rect)
        pygame.display.update()

    
    def draw_plate(self,screen,angle):
        # Rotate the plate and generate a new image.
        # Physics Engine and Control maintain angles in SI system. Visual uses angle in degrees.
        angle = np.rad2deg(angle)
        plate_new , plate_new_rect = rotate_image(self.plate,angle,self.plate_center) # Negative angle argument to ensure same coordinate system for ball and plate.
        

        # Blit the new image 
        screen.blit(plate_new,plate_new_rect)
        pygame.display.update()

        # Update Plate Angle
        self.plate_angle = angle

    def restart(self,plate_angle = 0):
        self.draw_plate(screen = screen, angle = plate_angle)
        

class Ball:
    def __init__(self):
        ## Loading Ball
        self.ball = pygame.image.load('Ball.png').convert()
        self.ball = pygame.transform.scale(self.ball,(90,90))
        self.ball.set_colorkey((0,0,0),0)
        self.ball_x_px_init = 804
        self.ball_y_px_init = 515
        self.scale = 1786 # 1786 px corresponds to 1 m

        screen.blit(self.ball,(self.ball_x_px_init,self.ball_y_px_init))
        pygame.display.update()

    def draw_ball(self,x,y):
        
        self.ball_x_px = self.scale * x + self.ball_x_px_init 
        self.ball_y_px = -self.scale * y + self.ball_y_px_init

        screen.blit(self.ball,(self.ball_x_px,self.ball_y_px))
        pygame.display.update()
    
    def restart(self,ball_pos_x = 0,ball_pos_y = 0):
        self.draw_ball(ball_pos_x,ball_pos_y)

class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.scoretext = self.font.render("Score " + str(self.score),1,(255,255,255))
        screen.blit(self.scoretext,(0,0))
        return

    def update_score(self):
        self.scoretext = self.font.render("Score " + str(self.score),1,(255,255,255))
        screen.blit(self.scoretext,(0,0))
        return

    def decrease_score(self):
        self.score = self.score - 1
        self.score = np.max(0,self.score)
        self.update_score()
        return
    def increase_score(self):
        self.score = self.score + 1
        self.update_score()


## Declaring Game Clock
clock = pygame.time.Clock()
simulation_terminate = False
       

if __name__=="__main__":
    # Loading the Plate
    plate = Plate()

    # Loading the Ball
    ball = Ball()

    # Initialising Physics Engine
    physics_engine = ball_plate_system(ball_radius = 0.025,plate_radius = 0.36 , mu = 0.02, ball_init_x = 0, ball_init_y = 0)

    # Initialsing Plate Controller
    plate_controller = pid_controller()
    machine_control = ml_controller()
    #plate_controller = simple_controller()

    # Initialising ScoreBoard
    scoreboard = Score()

    # Initialising the Terminal Condition Handler
    terminator = Terminator(physics_engine,plate_controller,plate,ball,scoreboard)

    
    # Declaring a Global Variable - I know. I must die in shame.

    simulation_record = False
    machine_play = False

    
    
    while simulation_terminate is not True:
        #print(physics_engine.ball_pos_x)
        
        if ((physics_engine.ball_pos_x < terminator.ball_limit_position_left) or (physics_engine.ball_pos_x > terminator.ball_limit_position_right)):
            terminator.terminal_condition_timer_active = False
            terminal_condition_timestamp = None
            scoreboard.decrease_score()
            terminator.restart_game()

        terminator.check_terminal_condition(physics_engine.ball_pos_x)
        terminator.check_timer()

        for event in pygame.event.get():
            
            ## Event Handling Conditions
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                sys.exit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
                if machine_play == False:
                    plate_controller.get_input('left')
                    if simulation_record == True :
                        copy_cat.writeData(physics_engine.ball_pos_x,physics_engine.ball_vel_x,physics_engine.plate_angle,1)
        
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                if machine_play == False:
                    plate_controller.get_input('right')
                    if simulation_record == True :
                        copy_cat.writeData(physics_engine.ball_pos_x,physics_engine.ball_vel_x,physics_engine.plate_angle,-1)

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                if machine_play == False:
                    plate_controller.get_input('center')
                    if simulation_record == True :
                        copy_cat.writeData(physics_engine.ball_pos_x,physics_engine.ball_vel_x,physics_engine.ball_acc,0)

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_s):
                copy_cat = DataLogger()
                copy_cat.initDataLogger()
                simulation_record = True
            
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_m):
                machine_play = True

        if machine_play == True:
            machine_control.gen_input(physics_engine.ball_pos_x,physics_engine.plate_angle,physics_engine.ball_vel_x)
            plate_controller.set_target(machine_control.control_input)    
            
        ## Query the controller for the angular velocity
        plate_angular_vel = plate_controller.control_loop()
        
        ## Feed angular velocity in the Physics Engine
        physics_engine.get_input(plate_angular_vel)
        ## Run the Physics Engine
        physics_engine.update()
        
        ## Render the graphics
        draw_background(screen,background_color)
        scoreboard.update_score()
        plate.draw_plate(screen=screen,angle=physics_engine.plate_angle)
        ball.draw_ball(x = physics_engine.ball_pos_x, y = physics_engine.ball_pos_y)
        ## Update the Controller
        plate_controller.get_observation(physics_engine.plate_angle)

        ## Set Frame Rate        
        clock.tick(30)


    