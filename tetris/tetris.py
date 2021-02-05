import pygame
from random import randint
import functools
import os

__dir__ = os.path.dirname(os.path.realpath(__file__))

### Константы
# Цвет заливки поля
COLOR_BACKGROUND = (255, 255, 255)
# Основной цвет текста
COLOR_FONT_BASE = (0, 0, 0)
# Дополнтительный цвет текста
COLOR_FONT_ALT  = (100, 100, 100)
# Ширина поля в ячейках
FIELD_WIDTH = 9
# Высота поля в ячейках. Поле с запасом, чтобы можно было генерить в (0, 0)
# фигуры и их не было видно
FIELD_HEIGHT = 25
# Размеры экрана в пикселях
SCREEN_WIDTH  = 590
SCREEN_HEIGHT = 960
# Мы обновляемся не каждый кадр, а с определенной частотой. Это позволяет
# двигать элементы поля не слишком быстро. Будем пропускать каждые
# TIME_SCALE миллисекунд
TIME_SCALE = 200
# Имя шрифта, которым будем рисовать все тексты на экране
FONT_BASE = 'Comic Sans MS'
CELL_SIZE = 44
COLORS = [
  (190, 0, 0, 255),
  (9, 35, 46, 255),
  (94, 47, 9, 255),
  (94, 66, 19, 255),
  (47, 75, 66, 255),
]

@functools.lru_cache(None)
def load_image(image):
    """
    Загружает каждую текстуру только один раз. Для последующих вызовов с тем же
    аргументом возвращает закэшированный результат.
    """
    print("load_image: loading " + image)
    image = os.path.join(__dir__, 'resources', image)
    image = pygame.image.load(image).convert_alpha()
    return image


def draw_field(screen, field, cell_size=CELL_SIZE):
  chip = load_image('chip.png')
  # Рисуем активные клетки
  for i in range(0, len(field)):
      row = field[i]
      for j in range(0, len(row)):
        cell = row[j]
        if cell > 0:
          # tint: красим картинку в нужный цвет
          c = chip.copy()
          c.fill(COLORS[cell - 1], special_flags=pygame.BLEND_RGBA_MULT)
          screen.blit(c, (j * cell_size, screen.get_height() - (len(field) - i) * cell_size))



def draw_cell(screen, position, color, cell_size = 10):
    """
    Рисует квадрат размером с клетку в заданной позиции (position) и заданным
    цветом (color)
    """
    x, y = position
    cell_width, cell_height = (cell_size, cell_size)
    cell = (x * cell_width, y * cell_height, cell_width, cell_height)
    pygame.draw.rect(screen, color, cell)
    # pygame.draw.polygon(screen, (0, 0, 0), [
    #   (x * cell_width, y * cell_height),
    #   ((x + 1) * cell_width, y * cell_height),
    #   ((x + 1) * cell_width, (y + 1) * cell_height),
    #   (x * cell_width, (y + 1), cell_height)
    # ], 2)


def draw(screen, field, score):
    """
    Функция для отрисовки игрового мира.
    """
    font = pygame.font.SysFont(FONT_BASE, 30)

    screen.blit(load_image("background.jpg"), (0, 0))
    # Поле рисуется отдельно, чтобы не сильно заморачиваться с вложенностью
    # координат "поле относительно экрана",
    # "клетка относительно поля относительно экрана", мы будем делать аналог
    # translate(dx, dy), которого в pygame нет. Но можно сделать с помощью blit
    field_width = 936
    field_height = 846
    field_surface = pygame.Surface((field_width, field_height), pygame.SRCALPHA, 32)
    field_surface.convert()
    field_surface.fill((0, 0, 0, 0))
    draw_field(field_surface, field)
    screen.blit(field_surface, (16, 92))

    hud_text = font.render(f'{score}', True, (99, 92, 71))
    screen.blit(hud_text, (537, 90))


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

def update(field, score, move_direction):
  return (field, score)

def run(screen):
    field = [[0] * FIELD_WIDTH for _ in range(0, FIELD_HEIGHT)]
    field[FIELD_HEIGHT - 1][0] = 1 # Тест
    field[FIELD_HEIGHT - 1][1] = 2 # Тест
    field[FIELD_HEIGHT - 1][2] = 3 # Тест
    field[FIELD_HEIGHT - 1][3] = 4 # Тест
    field[FIELD_HEIGHT - 1][3] = 5 # Тест

    field[0][0] = 1 # Тест
    field[0][1] = 2 # Тест
    field[0][2] = 3 # Тест
    field[0][3] = 1 # Тест
    score = 34
    move_direction = (0, 0)
    running = True

    while running:
        # Всегда обрабатываем пользовательский ввод и рисуем сцену.
        # Пользовательский ввод нужно обрабатывать, чтобы змейка была более
        # отзывчивой. Если пропускать этот шаг, то управление будет "лагать".
        move_direction, running = process_events(move_direction)

        if pygame.time.get_ticks() % TIME_SCALE != 0:
            continue

        draw(screen, field, score)
        pygame.display.flip()

        field, score = update(field, score, move_direction)
        # чистим направление, нужно только на один апдейт
        move_direction = (0, 0)

pygame.init()
pygame.font.init()
run(pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]))
pygame.quit()