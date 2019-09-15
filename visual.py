## This file will serve as a standard simulation visualisation module 


## Imports
import pygame
import sys
import time
from physics import ball_plate_system
from control import simple_controller
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
    

# Screen Properties
width=1800
height=960

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
        plate_new , plate_new_rect = rotate_image(self.plate,angle,self.plate_center)

        # Blit the new image 
        screen.blit(plate_new,plate_new_rect)
        pygame.display.update()

        # Update Plate Angle
        self.plate_angle = angle
class Ball:
    def __init__(self):
        ## Loading Ball
        self.ball = pygame.image.load('Ball.png').convert()
        self.ball = pygame.transform.scale(self.ball,(90,90))
        self.ball.set_colorkey((0,0,0),0)
        screen.blit(self.ball,(804,515))
        pygame.display.update()

    def draw_ball(self):
        screen.blit(self.ball,(804,515))
        pygame.display.update()





## Declaring Game Clock
clock = pygame.time.Clock()
    
simulation_terminate = False        

if __name__=="__main__":
    # Loading the Plate
    plate = Plate()

    # Loading the Ball
    ball = Ball()

    # Initialising Physics Engine
    physics_engine = ball_plate_system(ball_radius = 0.025,plate_radius = 0.36 , mu = 0.02)

    # Initialsing Plate Controller
    plate_controller = simple_controller()

    
    
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
        ball.draw_ball()
        ## Update the Controller
        plate_controller.get_observation(physics_engine.plate_angle)
        clock.tick(30)


    