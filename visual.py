## This file will serve as a standard simulation visualisation module 


## Imports
import pygame
import sys
import time
from physics import ball_plate_system
from control import *
import numpy as np
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

def restart_game(physics,control,plate,ball):
    physics.restart()
    control.restart()
    plate.restart()
    ball.restart()


    

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
        #print(angle)
        plate_new , plate_new_rect = rotate_image(self.plate,-angle,self.plate_center) # Negative angle argument to ensure same coordinate system for ball and plate.
        

        # Blit the new image 
        screen.blit(plate_new,plate_new_rect)
        pygame.display.update()

        # Update Plate Angle
        self.plate_angle = angle

    def restart(self):
        self.plate_angle = 0
        self.plate_rect = (245,600)
        screen.blit(self.plate,self.plate_rect)
        pygame.display.update()

class Ball:
    def __init__(self):
        ## Loading Ball
        self.ball = pygame.image.load('Ball.png').convert()
        self.ball = pygame.transform.scale(self.ball,(90,90))
        self.ball.set_colorkey((0,0,0),0)
        self.ball_init_x = 804
        self.ball_init_y = 515
        self.ball_x = 804
        self.ball_y = 515
        self.ball_x_px = 804
        self.ball_y_px = 515

        screen.blit(self.ball,(self.ball_init_x,self.ball_init_x))
        pygame.display.update()

    def draw_ball(self,x,y):
        xdelta = x - self.ball_x
        ydelta = y - self.ball_y

        self.ball_x_px = self.ball_x_px + xdelta/0.00056
        self.ball_y_px = self.ball_y_px + ydelta/0.00056
        screen.blit(self.ball,(self.ball_x_px,self.ball_y_px))
        pygame.display.update()

    def update(self,x,y):
        # Physics engine shares ball position x and y
        self.ball_x = x
        self.ball_y = y
    
    def restart(self):
        self.ball_x = self.ball_init_x
        self.ball_y = self.ball_init_y
        self.ball_x_px = self.ball_init_x
        self.ball_y_px = self.ball_init_y


## Declaring Game Clock
clock = pygame.time.Clock()
simulation_terminate = False
       

if __name__=="__main__":
    # Loading the Plate
    plate = Plate()

    # Loading the Ball
    ball = Ball()

    # Initialising Physics Engine
    physics_engine = ball_plate_system(ball_radius = 0.025,plate_radius = 0.36 , mu = 0.02, ball_init_x = ball.ball_init_x, ball_init_y = ball.ball_init_y)

    # Initialsing Plate Controller
    plate_controller = pid_controller()
    

    
    
    while simulation_terminate is not True:
        for event in pygame.event.get():
            
            ## Event Handling Conditions
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                sys.exit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
                plate_controller.get_input('left')
                

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                plate_controller.get_input('right')

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                plate_controller.get_input('center')
            
        ## Query the controller for the angular velocity
        plate_angular_vel = plate_controller.control_loop()
        
        ## Feed angular velocity in the Physics Engine
        physics_engine.get_input(plate_angular_vel)
        ## Run the Physics Engine
        physics_engine.update()
        
        ## Render the graphics
        draw_background(screen,background_color)
        plate.draw_plate(screen=screen,angle=physics_engine.plate_angle)
        ball.draw_ball(x = physics_engine.ball_pos_x, y = physics_engine.ball_pos_y)
        ## Update the Controller
        plate_controller.get_observation(physics_engine.plate_angle)

        ## Update the Graphic Variables
        ball.update(physics_engine.ball_pos_x,physics_engine.ball_pos_y)
        #print(clock.get_fps())

        if (ball.ball_x_px < 200 or ball.ball_x_px > 1590 ):
            restart_game(physics_engine,plate_controller,plate,ball)

        clock.tick(30)


    