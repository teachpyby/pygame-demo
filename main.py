import pygame
from random import randint
import uuid

pygame.init()

screen_size = 1000

alive_monsters = []

MAX_MONSTERS_COUNT = 20

def getMonster():
    monster = dict()
    monster['image'] = 'src/cat.png'
    monster['id'] = uuid.uuid4()
    return monster

monster_positions = dict()

def getMonsterNextPosition(monster, playerPosition):
    current_monster_position = monster_positions[monster['id']]
    if (current_monster_position is None):
        current_monster_position = getStartPosition()
    else:
        new_x_position = 0
        if current_monster_position[0] < playerPosition[0]:
            new_x_position = current_monster_position[0] + 1
        else:
            new_x_position = current_monster_position[0] - 1
        new_y_position = 0
        if current_monster_position[1] < playerPosition[1]:
            new_y_position = current_monster_position[1] + 1
        else:
            new_y_position = current_monster_position[1] - 1
        current_monster_position = (new_x_position, new_y_position)

    monster_positions[monster['id']] = current_monster_position

    return monster_positions[monster['id']]

def getStartPosition():
    edge = bool(randint(1, 4))
    if edge == 1:
        return (0, randint(0, screen_size))
    elif edge == 2:
        return (randint(0, screen_size), 0)
    elif edge == 3:
        return (screen_size, randint(0, screen_size))
    elif edge == 4:
        return (randint(0, screen_size), screen_size)

screen = pygame.display.set_mode([screen_size, screen_size])

running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))



    if (len(alive_monsters) < MAX_MONSTERS_COUNT):
        monster = getMonster()
        alive_monsters.append(monster)

    for monster in alive_monsters:
        # Draw a solid blue circle in the center
        # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)


    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

