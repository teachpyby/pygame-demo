import pygame
from random import randint
import uuid
import math
import os
import functools
from math import sqrt, sin

running = True

ticks_last = 0

# directions
# 0 - up
# 1 - left
# 2 - down
# 3 - right

nextDirection = 0


pygame.init()

# return if snake alive or not
# increase snake if snake eat an apple
def move_snake(snake, direction):
    return True

pixel_size = 20
screen_size = 1000
pixel_screen_size = screen_size / pixel_size

snake = [(pixel_screen_size / 2, pixel_screen_size - 1)]
screen      = pygame.display.set_mode([screen_size, screen_size])

while running:
    mouse_position  = pygame.mouse.get_pos()
    ticks_current   = pygame.time.get_ticks()
    ticks_delta     = ticks_current - ticks_last
    ticks_last      = ticks_current

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        nextDirection = 0
    elif keys[pygame.K_LEFT]:
        nextDirection = 1
    elif keys[pygame.K_DOWN]:
        nextDirection = 2
    elif keys[pygame.K_RIGHT]:
        nextDirection = 3


    screen.fill((255, 255, 255))

    for pixel in snake:
        pygame.draw.rect(screen, (0, 0, 0), (pixel[0] * pixel_size, pixel[1] * pixel_size, pixel_size, pixel_size) )

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

