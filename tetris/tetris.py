import pygame
from random import randint
import functools
import os
import sys

from pygame import math

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
FIELD_HEIGHT = 22
# Размеры экрана в пикселях
SCREEN_WIDTH  = 590
SCREEN_HEIGHT = 960 + 100 # убрать
# Мы обновляемся не каждый кадр, а с определенной частотой. Это позволяет
# двигать элементы поля не слишком быстро. Будем пропускать каждые
# TIME_SCALE миллисекунд
TIME_SCALE = 800 if sys.argv[1] is None else int(sys.argv[1])
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

def draw_figure(screen, figure_position, figure, cell_size=CELL_SIZE):
  chip = load_image('chip.png')
  for i in range(0, len(figure)):
    row = figure[i]
    for j in range(0, len(row)):
      cell = row[j]
      if cell > 0:
        y = screen.get_height() - (figure_position[0] - i + 1) * cell_size
        x = (j + figure_position[1]) * cell_size
        xy = (x, y)
        c = chip.copy()
        c.fill(COLORS[cell - 1], special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(c, xy)

def draw_field(screen, field, figure_position, figure_size, figure, cell_size=CELL_SIZE):
  row_font = pygame.font.SysFont(FONT_BASE, 30)
  position_font = pygame.font.SysFont(FONT_BASE, 10)

  chip = load_image('chip.png')
  # Рисуем поле
  for i in range(0, len(field)):
      row = field[i]
      y = screen.get_height() - (i + 1) * cell_size

      # debug номер ряда
      hud_text = row_font.render(f'{i}', True, (99, 92, 71))
      screen.blit(hud_text, (5, y))

      for j in range(0, len(row)):
        field_cell = row[j]
        xy = (j * cell_size, y)

        # debug номер позиции
        hud_text = position_font.render(f'{j}', True, (99, 92, 71))
        screen.blit(hud_text, xy)

        if field_cell > 0:
          # tint: красим картинку в нужный цвет
          c = chip.copy()
          c.fill(COLORS[field_cell - 1], special_flags=pygame.BLEND_RGBA_MULT)
          screen.blit(c, xy)



  x = figure_position[1] * cell_size
  y = screen.get_height() - (figure_position[0] + 1) * cell_size
  w = figure_size * cell_size
  h = figure_size * cell_size

  # debug прямоугольник
  pygame.draw.polygon(screen, (0, 0, 0), [
    (x, y), (x + w, y), (x + w, y + h), (x, y + h)
  ], 1)

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

def draw(screen, field, figure_position, figure_size, score, figure):
    """
    Функция для отрисовки игрового мира.
    """
    font = pygame.font.SysFont(FONT_BASE, 30)

    screen.blit(load_image("background.jpg"), (0, 150))
    # Поле рисуется отдельно, чтобы не сильно заморачиваться с вложенностью
    # координат "поле относительно экрана",
    # "клетка относительно поля относительно экрана", мы будем делать аналог
    # translate(dx, dy), которого в pygame нет. Но можно сделать с помощью blit
    field_width = 400
    field_height = 846 + 6 * CELL_SIZE
    field_surface = pygame.Surface((field_width, field_height), pygame.SRCALPHA, 32)
    field_surface.convert()
    field_surface.fill((50, 50, 50, 255))
    draw_field(field_surface, field, figure_position, figure_size, figure)
    draw_figure(field_surface, figure_position, figure)
    screen.blit(field_surface, (16, 92 - 6 * CELL_SIZE + 100))

    hud_text = font.render(f'{score}', True, (99, 92, 71))
    screen.blit(hud_text, (537, 90 + 100))


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
        move_direction = (0, 0)
    elif keys[pygame.K_LEFT]:
        move_direction = (0, -1)
    elif keys[pygame.K_DOWN]:
        move_direction = (0, 0)
    elif keys[pygame.K_RIGHT]:
        move_direction = (0, 1)

    return (move_direction, running)

start_figure_position = (20, 2)
FIGURE_SIZE = 4
def get_figure(t):
  # 0 - l
  if t == 1:
    return [
      [0, 0, t, 0],
      [0, 0, t, 0],
      [0, 0, t, 0],
      [0, 0, t, 0]
      ]
  # 1 - z
  elif t == 2:
    return [
      [0, t, t, 0],
      [0, 0, t, t],
      [0, 0, 0, 0],
      [0, 0, 0, 0]
      ]
  # 2 - T
  elif t == 3:
    return [
      [0, t, t, t],
      [0, 0, t, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0]
      ]
  # 3 - r
  elif t == 4:
    return [
      [0, 0, t, t],
      [0, 0, t, 0],
      [0, 0, t, 0],
      [0, 0, 0, 0]
      ]
  else:
    raise "ERR"

def update(field, figure_position, figure_size, figure, move_direction):
  if can_move(field, figure_position, figure, (0, move_direction[1])):
    figure_position = (figure_position[0], figure_position[1] + move_direction[1])
  if can_move(field, figure_position, figure, (-1, 0)):
    figure_position = (figure_position[0] - 1, figure_position[1])
    return (field, figure_position, figure)
  else:
    add_figure_to_field(field, figure_position, figure)
    return (field, start_figure_position, get_figure(randint(1, 4)))

def add_figure_to_field(field, figure_position, figure):
  for i in range(0, FIGURE_SIZE):
    for j in range(0, FIGURE_SIZE):
      i_f = figure_position[0] - i
      j_f = figure_position[1] + j
      if figure[i][j] > 0:
        field[i_f][j_f] = figure[i][j]

def can_move(field, figure_position, figure, direction):
  for i in range(0, FIGURE_SIZE):
    for j in range(0, FIGURE_SIZE):
      i_f = figure_position[0] - i
      j_f = figure_position[1] + j
      hit_vertical = direction[0] < 0 and i_f == 0
      hit_horizontal = direction[1] != 0 and j_f + direction[1] >= FIGURE_SIZE or j_f + direction[1] < 0 or field[i_f - direction[0]][j_f + direction[1]] > 0
      if figure[i][j] > 0 and (hit_horizontal or hit_vertical):
        return False
  return True


def run(screen):
    field = [[0] * FIELD_WIDTH for _ in range(0, FIELD_HEIGHT)]


    figure_position = start_figure_position
    figure = get_figure(1)

    score = 0
    move_direction = (0, 0)
    running = True

    while running:
        # Всегда обрабатываем пользовательский ввод и рисуем сцену.
        # Пользовательский ввод нужно обрабатывать, чтобы змейка была более
        # отзывчивой. Если пропускать этот шаг, то управление будет "лагать".
        move_direction, running = process_events(move_direction)

        if pygame.time.get_ticks() % TIME_SCALE != 0:
            continue

        draw(screen, field, figure_position, FIGURE_SIZE, score, figure)
        pygame.display.flip()

        print(move_direction)
        field, figure_position, figure = update(field, figure_position, FIGURE_SIZE, figure, move_direction)

        # # чистим направление, нужно только на один апдейт
        move_direction = (0, 0)

pygame.init()
pygame.font.init()
run(pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]))
pygame.quit()
