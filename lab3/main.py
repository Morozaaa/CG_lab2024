import pygame
import time

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 1200, 800
CELL_SIZE = 20  # Размер ячейки сетки
WHITE, BLACK, RED, GREEN, BLUE, ORANGE, GRAY = (
    (255, 255, 255),
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 165, 0),
    (200, 200, 200),
)

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Растровые алгоритмы")
clock = pygame.time.Clock()

def draw_grid():
    """Рисует сетку и оси координат."""
    screen.fill(WHITE)
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    # Оси координат
    pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)  # ось Y
    pygame.draw.line(screen, BLACK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)  # ось X

    # Подписи осей
    font = pygame.font.SysFont(None, 20)
    for x in range(-WIDTH // (2 * CELL_SIZE), WIDTH // (2 * CELL_SIZE) + 1):
        if x != 0:
            text = font.render(str(x), True, BLACK)
            screen.blit(text, (WIDTH // 2 + x * CELL_SIZE - 10, HEIGHT // 2 + 5))
    for y in range(-HEIGHT // (2 * CELL_SIZE), HEIGHT // (2 * CELL_SIZE) + 1):
        if y != 0:
            text = font.render(str(-y), True, BLACK)
            screen.blit(text, (WIDTH // 2 + 5, HEIGHT // 2 - y * CELL_SIZE - 10))

def draw_pixel(x, y, color=BLACK):
    """Рисует один пиксель, привязанный к сетке."""
    px = WIDTH // 2 + x * CELL_SIZE
    py = HEIGHT // 2 - y * CELL_SIZE
    pygame.draw.rect(screen, color, (px, py, CELL_SIZE, CELL_SIZE))

def step_by_step(x1, y1, x2, y2):
    """Пошаговый алгоритм растеризации."""
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    steps = max(dx, dy)
    x_step, y_step = (x2 - x1) / steps, (y2 - y1) / steps
    x, y = x1, y1
    calculations = f"Step-by-step: steps={steps}, x_step={x_step:.2f}, y_step={y_step:.2f}"
    for _ in range(steps + 1):
        draw_pixel(round(x), round(y), ORANGE)
        x += x_step
        y += y_step
    return calculations

def dda_line(x1, y1, x2, y2):
    """Реализация алгоритма ЦДА (DDA)."""
    dx, dy = x2 - x1, y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    x_inc, y_inc = dx / steps, dy / steps
    x, y = x1, y1
    calculations = f"DDA: dx={dx}, dy={dy}, steps={steps}, x_inc={x_inc:.2f}, y_inc={y_inc:.2f}"
    for _ in range(steps + 1):
        draw_pixel(round(x), round(y), RED)
        x += x_inc
        y += y_inc
    return calculations

def bresenham_line(x1, y1, x2, y2):
    """Реализация алгоритма Брезенхема для прямой."""
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    calculations = f"Bresenham Line: dx={dx}, dy={dy}, err={err}"
    while True:
        draw_pixel(x1, y1, GREEN)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return calculations

def bresenham_circle(xc, yc, r):
    """Реализация алгоритма Брезенхема для окружности."""
    x, y = 0, r
    d = 3 - 2 * r
    calculations = f"Bresenham Circle: Initial d={d}"
    while x <= y:
        for px, py in [(x, y), (y, x), (y, -x), (x, -y), (-x, -y), (-y, -x), (-y, x), (-x, y)]:
            draw_pixel(xc + px, yc + py, BLUE)
        x += 1
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
    return calculations

def measure_time(func, *args):
    """Замер времени выполнения функции."""
    start = time.time()
    calculations = func(*args)
    end = time.time()
    return end - start, calculations

# Однократные вычисления времени выполнения
step_time, step_calc = measure_time(step_by_step, -10, -5, 15, 10)
dda_time, dda_calc = measure_time(dda_line, -10, -5, 15, 10)
bresenham_time, bresenham_calc = measure_time(bresenham_line, -15, -10, 10, 5)
circle_time, circle_calc = measure_time(bresenham_circle, 0, 0, 10)

# Основной цикл программы
running = True
while running:
    draw_grid()

    # Отображение фиксированного времени и вычислений
    font = pygame.font.SysFont(None, 20)
    info_lines = [
        f"Step-by-step (Orange): {step_time:.6f}s | {step_calc}",
        f"DDA (Red): {dda_time:.6f}s | {dda_calc}",
        f"Bresenham Line (Green): {bresenham_time:.6f}s | {bresenham_calc}",
        f"Bresenham Circle (Blue): {circle_time:.6f}s | {circle_calc}",
        "Целочисленные координаты привязаны к дискретной сетке через масштабирование.",
        f"Масштаб: 1 логическая единица = {CELL_SIZE} пикселей на экране."
    ]
    for i, line in enumerate(info_lines):
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (10, 10 + i * 20))

    # Рисование фигур
    step_by_step(-10, -5, 15, 10)
    dda_line(-10, -5, 15, 10)
    bresenham_line(-15, -10, 10, 5)
    bresenham_circle(0, 0, 10)

    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
