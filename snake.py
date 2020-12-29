import pygame
from random import randint

### Константы
# Цвет заливки поля
COLOR_BACKGROUND = (255, 255, 255)
# Цвет змеи
COLOR_SNAKE = (31, 47, 26)
# Цвет яблока
COLOR_APPLE = (164, 0, 0)
# Основной цвет текста
COLOR_FONT_BASE = (0, 0, 0)
# Дополнтительный цвет текста
COLOR_FONT_ALT  = (100, 100, 100)
# Ширина поля в ячейках
FIELD_WIDTH = 50
# Высота поля в ячейках
FIELD_HEIGHT = 50
# Размеры экрана в пикселях
SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 1000
# Размеры ячейки в пикселях. Нужны для отрисовки элементов поля: змея, яблоко
CELL_SIZE = (SCREEN_WIDTH / FIELD_WIDTH, SCREEN_HEIGHT / FIELD_HEIGHT)
# Задает ориентацию и длинну змеи на старте игры. Позиция змеи задается ниже
# При расчете размеров экрана
SNAKE_INITIAL = [(0, 0), (0, 1), (0, 1)]
# Мы обновляемся не каждый кадр, а с определенной частотой. Это позволяет
# двигать змею не слишком быстро. Будем пропускать каждые TIME_SCALE миллисекунд
TIME_SCALE = 50
# Имя шрифта, которым будем рисовать все тексты на экране
FONT_BASE = 'Comic Sans MS'

def move_snake(snake, direction, apple, field_width, field_height):
    """
    Перемещает змею в указанном направлении.

    Змея описывается списком пар (x, y). Каждая пара это координата в клетках
    поля. direction задает направление перемещения змеи по полю. И описывается
    так же парой координат (dx, dy).

    apple - задает позицию яблока на поле. Когда змея съедает яблоко, то
    увеличивается на 1 клетку.

    Функция должна вернуть tuple из трех элементов:
    * Список описывающий змею
    * Флаг True или False. Значение показывает жива ли змея
    * Позиция яблока. Если змея съела яблоко на текущем ходу, то возвращает
      новую позицию яблока
    """

    head = snake[0]
    new_head_x = (head[0] + direction[0]) % field_width
    new_head_y = (head[1] + direction[1]) % field_height
    new_head = (new_head_x, new_head_y)
    snake.insert(0, new_head)

    if new_head == apple:
        # Съели яблоко, поэтому генерируем новое и не убираем хвост
        apple = (randint(0, field_width - 1), randint(0, field_height - 1))
    else:
        # Удаляем хвост и так эмулируем перемещение.
        snake.pop(len(snake) - 1)

    return (snake, new_head not in snake[1:], apple)

def draw_cell(screen, position, color):
    """
    Рисует квадрат размером с клетку в заданной позиции (position) и заданным
    цветом (color)
    """
    x, y = position
    cell_width, cell_height = CELL_SIZE
    cell = (x * cell_width, y * cell_height, cell_width, cell_height)
    pygame.draw.rect(screen, color, cell)


def draw(screen, snake, is_alive, apple):
    """
    Функция для отрисовки игрового мира.
    """
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    score = len(snake) - len(SNAKE_INITIAL)
    font = pygame.font.SysFont(FONT_BASE, 30)

    screen.fill(COLOR_BACKGROUND)
    draw_cell(screen, apple, COLOR_APPLE)
    for pixel in snake:
        draw_cell(screen, pixel, COLOR_SNAKE)

    if not is_alive:
        game_over_text = font.render(f'Game Over. Your score is {score}', \
                                     True, COLOR_FONT_BASE)
        screen_center = (screen_width / 2 - game_over_text.get_width() / 2, \
                         screen_height / 2)
        screen.blit(game_over_text, screen_center)

    hud_text = font.render(f'Score: {score}', True, COLOR_FONT_ALT)
    screen.blit(hud_text, (10, 10))

def process_events(move_direction):
    """
    Функция обрабатывающая пользовательский ввод.
    Нам нужно определить в какую сторону теперь двигается змейка. Если
    пользователь нажимает на стрелки, то move_direction меняется на
    соответствующий. Если же пользователь ничего не делает, то move_direction
    возвращается без изменений.

    Если пользователь нажимает кнопку ESC, то функция вернет вторым значением
    False. Иначе будет True. Это значение показывает продолжать ли обновление
    игры.
    """

    running = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        move_direction = (0, -1)
    elif keys[pygame.K_LEFT]:
        move_direction = (-1, 0)
    elif keys[pygame.K_DOWN]:
        move_direction = (0, 1)
    elif keys[pygame.K_RIGHT]:
        move_direction = (1, 0)

    return (move_direction, running)

def run(screen):
    # Инициализируем стартовое состояние игры:
    #  * Яблоко в центре поля
    #  * Змейка левее яблока на клетку
    #  * Змейка ползет в сторону яблока
    apple = (FIELD_WIDTH / 2, FIELD_HEIGHT / 2)
    snake = [(x + apple[0] - 2, y + apple[1]) for x, y in SNAKE_INITIAL]
    move_direction = (1, 0)
    is_alive = True
    move = 0

    running = True
    ticks_last = 0

    while running:
        # Всегда обрабатываем пользовательский ввод и рисуем сцену.
        # Пользовательский ввод нужно обрабатывать, чтобы змейка была более
        # отзывчивой. Если пропускать этот шаг, то управление будет "лагать".
        move_direction, running = process_events(move_direction)

        if pygame.time.get_ticks() % TIME_SCALE != 0:
            continue

        draw(screen, snake, is_alive, apple)
        pygame.display.flip()

        # Игровая логика расчината на то, что змейка перемещается "шагами".
        # Значит нам нужно пропускать равные промежутки времени между
        # обновлениями позиции змейки.
        if is_alive:
            snake, is_alive, apple = move_snake(snake, move_direction, apple, \
                                     FIELD_WIDTH, FIELD_HEIGHT)
            print(f'{move}: Head {snake[0]}. Direction: {move_direction}. Apple: {apple}')
            move += 1

pygame.init()
pygame.font.init()
run(pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]))
pygame.quit()