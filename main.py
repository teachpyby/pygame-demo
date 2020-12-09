import pygame
from random import randint
import uuid
import math
import os
from math import sqrt, sin

BLACK = (0, 0, 0)
MAX_MONSTERS_COUNT = 20
BASE_PATH = os.path.dirname(__file__)
base_path = BASE_PATH
screen_size = 1000

MONSTERS = [
    'Hitman 1/hitman1_silencer.png',
    'Man Blue/manBlue_silencer.png',
    'Robot 1/robot1_silencer.png'
]

def load_sprite(name, x = 0, y = 0):
    img = os.path.join(BASE_PATH, 'resources', 'PNG', name)
    return { 'x': x, 'y': y,
             'dx': 0, 'dy': 0,
             'rotate': 0,
             'image': pygame.image.load(img) }

def get_monster_next_position(monster, player_position, timestamp):
    update_modifier = 1 if timestamp % 5 == 0 else 0
    current_monster_position = (monster['x'], monster['y'])
    new_x_position = 0
    if current_monster_position[0] < player_position[0]:
        new_x_position = current_monster_position[0] + 1 * update_modifier
    else:
        new_x_position = current_monster_position[0] - 1 * update_modifier
    new_y_position = 0
    if current_monster_position[1] < player_position[1]:
        new_y_position = current_monster_position[1] + 1 * update_modifier
    else:
        new_y_position = current_monster_position[1] - 1 * update_modifier

    return (new_x_position, new_y_position)

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

timestamp = 0
screen = pygame.display.set_mode([screen_size, screen_size])

def get_bullet(shooter):
    bullet = dict()
    bullet['target'] = pos
    bullet['start_position'] = shooter
    bullet['current_position'] = shooter
    return bullet

def update_bullets_position(bullets):
    bullet_speed = 3
    for bullet in bullets:
        dx = bullet['target'][0] - bullet['start_position'][0]
        dy = bullet['target'][1] - bullet['start_position'][1]
        dist = sqrt(dx ** 2 + dy ** 2)
        bullet['current_position'] = (bullet['current_position'][0] + (dx / dist) * bullet_speed, bullet['current_position'][1] + (dy / dist) * bullet_speed)
    return bullets

def rotate_angle(dst_position, sprite):
    """
    Определяет угол, на который нужно повернуть спрайт, чтобы тот был ориентирован
    в определенную точку.
    """
    position = (sprite['x'], sprite['y'])
    vec = (dst_position[0] - position[0], dst_position[1] - position[1])
    orientation = (1, 0)
    mul = vec[0] * orientation[0] + vec[1] * orientation[1]
    len = sqrt(vec[0] ** 2 + vec[1] ** 2)

    if len == 0:
        return sprite['rotate']

    cos_a = mul / len
    sign = 0 if vec[1] == 0 else vec[1] / abs(vec[1])
    return (-1 * sign) * math.acos(cos_a) * 180 / math.pi

pygame.init()
screen_size = 1000

running = True
monster_positions = dict()
alive_monsters = []
bullets = []

shooter = load_sprite('Woman Green/womanGreen_machine.png',
                      x = screen_size / 2, y = screen_size / 2)

world = []
world.append(shooter)

while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            bullets.append(get_bullet((shooter['x'], shooter['y'])))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        shooter['x'] = shooter['x'] + 1
    elif keys[pygame.K_a]:
        shooter['x'] = shooter['x'] - 1
    elif keys[pygame.K_w]:
        shooter['y'] = shooter['y'] - 1
    elif keys[pygame.K_s]:
        shooter['y'] = shooter['y'] + 1

    shooter['rotate'] = rotate_angle(pygame.mouse.get_pos(), shooter)

    # Fill the background with white
    screen.fill((255, 255, 255))

    if len(alive_monsters) < MAX_MONSTERS_COUNT:
        spawn_x, spawn_y = get_start_position()
        monster = load_sprite(MONSTERS[randint(0, len(MONSTERS) - 1)], x = spawn_x, y = spawn_y)
        alive_monsters.append(monster)
        world.append(monster)

    bullets = update_bullets_position(bullets)
    for bullet in bullets:
        pygame.draw.circle(screen, BLACK, bullet['current_position'], 2)

    for monster in alive_monsters:
        player_position = (shooter['x'], shooter['y'])
        monster_position = get_monster_next_position(monster, player_position, timestamp)
        monster['x'] = monster_position[0]
        monster['y'] = monster_position[1]
        monster['rotate'] = rotate_angle((shooter['x'], shooter['y']), monster)

    for e in world:
        image = e['image']
        rotated_image = pygame.transform.rotate(image, e['rotate'])
        rorated_rect = rotated_image.get_rect(center = image.get_rect(center = (e['x'], e['y'])).center)

        screen.blit(rotated_image, rorated_rect.topleft)

    # Flip the display
    timestamp = (timestamp + 1) % 5

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

