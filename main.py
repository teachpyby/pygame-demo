import pygame
from random import randint
import uuid
import math
import os
from math import sqrt, sin

BLACK = (0, 0, 0)
MAX_MONSTERS_COUNT = 20
BASE_PATH = os.path.dirname(__file__)

NPC_SPEED        = 0.05
PROJECTILE_SPEED = 5

BULLET = lambda pos: pygame.draw.circle(screen, BLACK, pos, 2)

MONSTERS = [
    'Hitman 1/hitman1_silencer.png',
    'Man Blue/manBlue_silencer.png',
    'Robot 1/robot1_silencer.png'
]

### Sprite

def sprite_load(x = 0, y = 0, image = None, draw_fn = None):
    """
    Создает спрайт по позиции и имени картинки. Загружая текстуру из
    resources/PNG. Вместо текстуры можно использовать draw_fn - функцию, которая
    принимает позицию и рисует что-то на экране.
    """
    if image:
        image = os.path.join(BASE_PATH, 'resources', 'PNG', image)
        image = pygame.image.load(image)

    return { 'x': x, 'y': y, 'rotate': 0,
             'image':  image, 'draw_fn': draw_fn }

def sprite_position(sprite):
    """
    Метод для удобного получения позиции спрайта в виде tuple. Tuples
    неизменяемые и их удобно передавать в другие методы. Но позицию спрайта
    удобно держать отдельными полями в dict.
    """
    return (sprite['x'], sprite['y'])

def sprite_draw(sprite):
    """
    Рисует спрайт на канвасе в указанной точке. Спрайт может быть картинкой.
    Может быть функцией,которая что-то нарисует. В этом случае смотрим
    содержимое по ключу 'draw_fn'. Функция принимает единственный аргумент:
    position.
    """
    image = sprite['image']
    draw_fn = sprite['draw_fn']
    position = sprite_position(sprite)

    if image:
        image_center = image.get_rect(center = position).center
        rotated_image = pygame.transform.rotate(image, sprite['rotate'])
        rorated_rect = rotated_image.get_rect(center = image_center)
        screen.blit(rotated_image, rorated_rect.topleft)
    elif draw_fn:
        draw_fn(position)

def sprite_box(sprite):
    """
    Возвращает bounding box спрайта
    """
    image = sprite['image']
    position = sprite_position(sprite)
    image_center = image.get_rect(center = position).center
    rotated_image = pygame.transform.rotate(image, sprite['rotate'])
    return rotated_image.get_rect(center = image_center)

def sprite_aim(sprite, dst_position):
    """
    Определяет угол, на который нужно повернуть спрайт, чтобы тот был
    ориентирован в определенную точку.
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
    return -1  * sign * math.acos(cos_a) * 180 / math.pi

def sprite_dispose(sprite):
    return sprite.get('dispose', False)

### NPC

def npc_update(t, npc, player):
    """
    Обновляет позицию NPC так, чтобы тот двигался в сторону игрока. Так же
    поворачивает NPC в этом направлении.
    """
    player_position = sprite_position(player)
    npc_position    = sprite_position(npc)

    dx = player_position[0] - npc_position[0]
    dy = player_position[1] - npc_position[1]
    r  = sqrt(dx ** 2 + dy ** 2)
    dr = t * NPC_SPEED

    dx0 = dx / r * dr
    dy0 = dy / r * dr

    npc['x'] = npc['x'] + dx0
    npc['y'] = npc['y'] + dy0

    npc['rotate'] = sprite_aim(npc, player_position)

def npc_spawn_position():
    edge = randint(1, 4)

    if edge == 1:
        return (0, randint(0, screen_size))
    elif edge == 2:
        return (randint(0, screen_size), 0)
    elif edge == 3:
        return (screen_size, randint(0, screen_size))
    elif edge == 4:
        return (randint(0, screen_size), screen_size)

### Projectiles

def projectile_spawn(player, aim, draw_fn):
    x, y = sprite_position(player)

    dx = aim[0] - x
    dy = aim[1] - y
    r  = sqrt(dx ** 2 + dy ** 2)

    projectile = sprite_load(x = x, y = y, draw_fn = draw_fn)
    projectile['dx'] = dx / r
    projectile['dy'] = dy / r

    return projectile

screen_size = 1000
screen      = pygame.display.set_mode([screen_size, screen_size])

# Количество тиков со старта на последнем кадре
ticks_last  = 0
# Обновляем игру пока True
running     = True
# Список объектов в мире. Наш основной список для отрисовки
world       = []
# Список NPC. Нужен для того чтобы обновлять NPC
npcs        = []
# Список Projectiles. Все что вылетает из пушек.
projectiles = []
# Игрок
player      = sprite_load(image = 'Woman Green/womanGreen_machine.png',
                          x = screen_size / 2, y = screen_size / 2)
world.append(player)

pygame.init()
while running:
    mouse_position  = pygame.mouse.get_pos()
    ticks_current   = pygame.time.get_ticks()
    ticks_delta     = ticks_current - ticks_last
    ticks_last      = ticks_current

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            projectile = projectile_spawn(player, mouse_position, BULLET)
            projectiles.append(projectile)
            world.append(projectile)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player['x'] = player['x'] + 1
    elif keys[pygame.K_a]:
        player['x'] = player['x'] - 1
    elif keys[pygame.K_w]:
        player['y'] = player['y'] - 1
    elif keys[pygame.K_s]:
        player['y'] = player['y'] + 1

    player['rotate'] = sprite_aim(player, pygame.mouse.get_pos())

    if len(npcs) < MAX_MONSTERS_COUNT:
        spawn_x, spawn_y = npc_spawn_position()
        npc_image = MONSTERS[randint(0, len(MONSTERS) - 1)]
        monster = sprite_load(image = npc_image, x = spawn_x, y = spawn_y)
        npcs.append(monster)
        world.append(monster)

    screen_box = pygame.Rect(0, 0, screen_size, screen_size)
    for projectile in projectiles:
        projectile['x'] = projectile['x'] + projectile['dx'] * PROJECTILE_SPEED
        projectile['y'] = projectile['y'] + projectile['dy'] * PROJECTILE_SPEED

        if not screen_box.collidepoint(projectile['x'], projectile['y']):
            projectile['dispose'] = True

        for npc in npcs:
            if sprite_box(npc).collidepoint(projectile['x'], projectile['y']):
                npc['dispose'] = True

    for npc in npcs:
        npc_update(ticks_delta, npc, player)

    npcs        = [n for n in npcs if not sprite_dispose(n)]
    projectiles = [p for p in projectiles if not sprite_dispose(p)]
    world       = [w for w in world if not sprite_dispose(w)]
    ##### Draw
    # Fill the background with white
    screen.fill((255, 255, 255))

    for e in world:
        sprite_draw(e)

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

