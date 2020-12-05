import pygame
from random import randint
import uuid
import os

base_path = os.path.dirname(__file__)
pygame.init()
BLACK = (0, 0, 0)

screen_size = 1000

alive_monsters = []

MAX_MONSTERS_COUNT = 20

def get_monster():
    monster = dict()
    monster['image'] = 'resources/PNG/Woman Green/womanGreen_machine.png'
    monster['id'] = uuid.uuid4().__str__()
    return monster

monster_positions = dict()

def get_monster_next_position(monster, playerPosition, timestamp):
    has_position = monster['id'] in monster_positions
    current_monster_position = (0, 0)
    if (has_position == False):
        current_monster_position = get_start_position()
    else:
        update_modifier = 1 if timestamp % 5 == 0 else 0
        current_monster_position = monster_positions[monster['id']]
        new_x_position = 0
        if current_monster_position[0] < playerPosition[0]:
            new_x_position = current_monster_position[0] + 1 * update_modifier
        else:
            new_x_position = current_monster_position[0] - 1 * update_modifier
        new_y_position = 0
        if current_monster_position[1] < playerPosition[1]:
            new_y_position = current_monster_position[1] + 1 * update_modifier
        else:
            new_y_position = current_monster_position[1] - 1 * update_modifier
        current_monster_position = (new_x_position, new_y_position)

    monster_positions[monster['id']] = current_monster_position

    return monster_positions[monster['id']]

timestamp = 0

def get_start_position():
    edge = randint(1, 4)
    if edge == 1:
        return (0, randint(0, screen_size))
    elif edge == 2:
        return (randint(0, screen_size), 0)
    elif edge == 3:
        return (screen_size, randint(0, screen_size))
    elif edge == 4:
        return (randint(0, screen_size), screen_size)

screen = pygame.display.set_mode([screen_size, screen_size])

shooter = dict()
shooter['id'] = uuid.uuid4().__str__()
shooter['image'] = 'resources/PNG/Woman Green/womanGreen_machine.png'

shooter_position = (screen_size / 2, screen_size / 2)
bullets = []

running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            bullet = dict()
            bullet['target'] = pos
            bullet['start_position'] = shooter_position
            bullet['current_position'] = shooter_position
            bullets.append(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        shooter_position = (shooter_position[0] + 1, shooter_position[1])
    if keys[pygame.K_a]:
        shooter_position = (shooter_position[0] - 1, shooter_position[1])
    if keys[pygame.K_w]:
        shooter_position = (shooter_position[0], shooter_position[1] - 1)
    if keys[pygame.K_s]:
        shooter_position = (shooter_position[0], shooter_position[1] + 1)


    # Fill the background with white
    screen.fill((255, 255, 255))

    if (len(alive_monsters) < MAX_MONSTERS_COUNT):
        monster = get_monster()
        alive_monsters.append(monster)

    for bullet in bullets:
        pygame.draw.circle(screen, BLACK, bullet['current_position'], 2)

    for monster in alive_monsters:
        monster_image_path = os.path.join(base_path, shooter['image'])
        monster_position = get_monster_next_position(monster, shooter_position, timestamp)
        screen.blit(pygame.image.load(monster_image_path), monster_position)

    path = os.path.join(base_path, shooter['image'])
    screen.blit(pygame.image.load(path), shooter_position)

    # Flip the display
    timestamp = (timestamp + 1) % 5

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

