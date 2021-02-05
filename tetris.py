import pygame
from random import randint

### Константы
# Цвет заливки поля
COLOR_BACKGROUND = (255, 255, 255)
# Основной цвет текста
COLOR_FONT_BASE = (0, 0, 0)
# Дополнтительный цвет текста
COLOR_FONT_ALT  = (100, 100, 100)
# Ширина поля в ячейках
FIELD_WIDTH = 50
# Высота поля в ячейках
FIELD_HEIGHT = 80
# Размеры экрана в пикселях
SCREEN_WIDTH  = 680
SCREEN_HEIGHT = 940
# Мы обновляемся не каждый кадр, а с определенной частотой. Это позволяет
# двигать элементы поля не слишком быстро. Будем пропускать каждые
# TIME_SCALE миллисекунд
TIME_SCALE = 200
# Имя шрифта, которым будем рисовать все тексты на экране
FONT_BASE = 'Comic Sans MS'
CELL_SIZE = 10
COLORS = [(255, 0, 0)]


def draw_field(screen, field, cell_size=CELL_SIZE):
  field_width = screen.get_width()
  field_height = screen.get_height()
  screen.fill((255, 255, 255))

  field_cells = pygame.Surface((field_width - 4, field_height - 4))
  field_cells.fill((255, 255, 255))
  # Рисуем активные клетки
  for i in range(0, len(field)):
      row = field[i]
      for j in range(0, len(row)):
        cell = row[j]
        if cell > 0:
          draw_cell(field_cells, (j, i), COLORS[cell - 1], cell_size=cell_size)

  screen.blit(field_cells, (2, 2))
  pygame.draw.polygon(screen, (0, 0, 0), [
      (2, 0), (field_width - 2, 0),
      (field_width - 2, field_height - 2),
      (2, field_height - 2)
    ], 2)



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
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    font = pygame.font.SysFont(FONT_BASE, 30)

    screen.fill(COLOR_BACKGROUND)

    # Поле рисуется отдельно, чтобы не сильно заморачиваться с вложенностью
    # координат "поле относительно экрана",
    # "клетка относительно поля относительно экрана", мы будем делать аналог
    # translate(dx, dy), которого в pygame нет. Но можно сделать с помощью blit
    field_width = FIELD_WIDTH * CELL_SIZE
    field_height = FIELD_HEIGHT * CELL_SIZE
    field_surface = pygame.Surface((field_width + 4, field_height + 4))
    draw_field(field_surface, field)
    screen.blit(field_surface, (20, screen_height - field_height - 20))

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

def update(field, score):
  return (field, score)

def run(screen):
    field = [[0] * FIELD_WIDTH for _ in range(0, FIELD_HEIGHT)]
    field[FIELD_HEIGHT - 1][0] = 1 # Тест
    field[FIELD_HEIGHT - 1][1] = 1 # Тест
    field[FIELD_HEIGHT - 1][2] = 1 # Тест
    field[FIELD_HEIGHT - 1][3] = 1 # Тест

    field[5][0] = 1 # Тест
    field[5][1] = 1 # Тест
    field[5][2] = 1 # Тест
    field[5][3] = 1 # Тест
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

        draw(screen, field, score)
        pygame.display.flip()

        field, score = update(field, score)

pygame.init()
pygame.font.init()
run(pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]))
pygame.quit()