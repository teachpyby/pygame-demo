import pygame
from random import randint
import uuid
import math
import os
import functools
from math import sqrt, sin

running = True

ticks_last = 0
move_direction = 0

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


# directions
# 0 - up
# 1 - left
# 2 - down
# 3 - right


# return if snake alive or not
# increase snake if snake eat an apple
# snake - coordinates of snake
# direction - direction of snake move
# apple - coordinates of an apple
def move_snake(snake, direction, apple):
    return (snake, True, apple)

def get_apple():
    return (screen_size / 2, screen_size / 2)

pixel_size = 20
screen_size = 1000
pixel_screen_size = screen_size / pixel_size

snake = [(pixel_screen_size / 2, pixel_screen_size - 1)]
screen      = pygame.display.set_mode([screen_size, screen_size])
apple = None
is_alive = False

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
        move_direction = 0
    elif keys[pygame.K_LEFT]:
        move_direction = 1
    elif keys[pygame.K_DOWN]:
        move_direction = 2
    elif keys[pygame.K_RIGHT]:
        move_direction = 3

    screen.fill((255, 255, 255))

    if is_alive:
        res = move_snake(snake, move_direction, apple)
        snake = res[0]
        is_alive = res[1]
        apple = res[2]

    if apple is None:
        apple = get_apple()

    if is_alive:
        for pixel in snake:
            pygame.draw.rect(screen, (0, 0, 0), (pixel[0] * pixel_size, pixel[1] * pixel_size, pixel_size, pixel_size) )
    else:
        game_over_text = myfont.render(f'Game Over. Your score is {len(snake)}', False, (0, 0, 0))
        screen.blit(game_over_text,(screen_size/2 - game_over_text.get_width() / 2, screen_size/2))
        screen.blit(game_over_text,(screen_size/2 - game_over_text.get_width() / 2, screen_size/2))

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

