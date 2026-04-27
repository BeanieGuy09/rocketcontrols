import sys
import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((500, 500), 0, 32)
clock = pygame.time.Clock()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# Square setup
square_size = 50
my_square = pygame.Rect(0, 0, square_size, square_size)
my_square_color = 0
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Center of the screen
CENTER = (250, 250)
# Max distance the square can move from center
MAX_DISTANCE = 200 

# Track input from both sticks
# [Left Stick X, Left Stick Y, Right Stick X, Right Stick Y]
inputs = [0.0, 0.0, 0.0, 0.0]

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN:
            if event.button == 0:
                my_square_color = (my_square_color + 1) % len(colors)
        
        if event.type == JOYAXISMOTION:
            # Axis 0,1 = Left Stick | Axis 2,3 (usually) = Right Stick
            if event.axis < 4:
                inputs[event.axis] = event.value

        if event.type == JOYDEVICEADDED or event.type == JOYDEVICEREMOVED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    # --- LOGIC ---
    
    # 1. Start at the center
    target_x = CENTER[0]
    target_y = CENTER[1]

    # 2. Add Left Stick movement (Full distance)
    # Deadzone check for better feel
    lx = inputs[0] if abs(inputs[0]) > 0.1 else 0
    ly = inputs[1] if abs(inputs[1]) > 0.1 else 0
    
    target_x += lx * MAX_DISTANCE
    target_y += ly * MAX_DISTANCE

    # 3. Add Right Stick movement (Half distance)
    rx = inputs[2] if abs(inputs[2]) > 0.1 else 0
    ry = inputs[3] if abs(inputs[3]) > 0.1 else 0
    
    target_x += rx * (MAX_DISTANCE * 0.5)
    target_y += ry * (MAX_DISTANCE * 0.5)

    # Update square position (adjusting for center of the square)
    my_square.centerx = target_x
    my_square.centery = target_y

    # --- DRAW ---
    pygame.draw.rect(screen, colors[my_square_color], my_square)
    pygame.display.update()
    clock.tick(60)