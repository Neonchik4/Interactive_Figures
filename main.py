import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800  # Ширина экрана
SCREEN_HEIGHT = 600  # Высота экрана
FPS = 120  # Частота кадров в секунду

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Интерактивные фигуры")


# Класс для фигур
class Shape:
    def __init__(self, x, y, shape_type, color):
        self.x = x  # Координата X
        self.y = y  # Координата Y
        self.shape_type = shape_type  # Тип фигуры (круг, квадрат, треугольник, шестиугольник)
        self.color = color  # Цвет фигуры
        self.is_dragged = False  # Флаг для проверки перетаскивания
        self.offset_x = 0  # Смещение по X относительно позиции курсора
        self.offset_y = 0  # Смещение по Y относительно позиции курсора

    # Функция для рисования фигуры
    def draw(self):
        if self.shape_type == "circle":
            pygame.draw.circle(screen, self.color, (self.x, self.y), 40)
        elif self.shape_type == "square":
            pygame.draw.rect(screen, self.color, (self.x - 40, self.y - 40, 80, 80))
        elif self.shape_type == "triangle":
            points = [(self.x, self.y - 50), (self.x - 45, self.y + 30), (self.x + 45, self.y + 30)]
            pygame.draw.polygon(screen, self.color, points)
        elif self.shape_type == "hexagon":
            angle = math.pi / 3  # Угол для построения шестиугольника
            points = [(self.x + 40 * math.cos(i * angle), self.y + 40 * math.sin(i * angle)) for i in range(6)]
            pygame.draw.polygon(screen, self.color, points)


# Список фигур
shapes = []
dragged_shape = None  # Флаг для отслеживания перетаскиваемой фигуры

# Основной игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((255, 255, 255))  # Заполнение экрана белым цветом

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Выход из игры
            running = False
        elif event.type == pygame.KEYDOWN:  # Нажатие клавиши
            # Создание фигур по нажатию клавиш
            r_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if event.key == pygame.K_1:
                shapes.append(
                    Shape(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50),
                          "circle", r_color))
            elif event.key == pygame.K_2:
                shapes.append(
                    Shape(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50),
                          "square", r_color))
            elif event.key == pygame.K_3:
                shapes.append(
                    Shape(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50),
                          "triangle", r_color))
            elif event.key == pygame.K_4:
                shapes.append(
                    Shape(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50),
                          "hexagon", r_color))
            elif event.key == pygame.K_SPACE:  # Удаление последней добавленной фигуры
                if shapes:  # Проверяем, есть ли фигуры
                    shapes.pop()  # Удаляем последнюю фигуру из списка
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Нажатие кнопки мыши
            for shape in reversed(shapes):  # Проверка, какая фигура была нажата
                if shape.shape_type == "circle" and math.hypot(shape.x - event.pos[0], shape.y - event.pos[1]) < 40:
                    shape.is_dragged = True  # Отметить фигуру как перетаскиваемую
                    shape.offset_x = shape.x - event.pos[0]  # Рассчитать смещение по X
                    shape.offset_y = shape.y - event.pos[1]  # Рассчитать смещение по Y
                    dragged_shape = shape  # Запоминаем перетаскиваемую фигуру
                    break
                elif shape.shape_type == "square" and shape.x - 40 <= event.pos[0] <= shape.x + 40 and shape.y - 40 <= \
                        event.pos[1] <= shape.y + 40:
                    shape.is_dragged = True
                    shape.offset_x = shape.x - event.pos[0]
                    shape.offset_y = shape.y - event.pos[1]
                    dragged_shape = shape
                    break
                elif shape.shape_type == "triangle":
                    triangle_points = [(shape.x, shape.y - 50), (shape.x - 45, shape.y + 30),
                                       (shape.x + 45, shape.y + 30)]
                    if pygame.draw.polygon(screen, (0, 0, 0, 0), triangle_points).collidepoint(event.pos):
                        shape.is_dragged = True
                        shape.offset_x = shape.x - event.pos[0]
                        shape.offset_y = shape.y - event.pos[1]
                        dragged_shape = shape
                        break
                elif shape.shape_type == "hexagon":
                    angle = math.pi / 3
                    points = [(shape.x + 40 * math.cos(i * angle), shape.y + 40 * math.sin(i * angle)) for i in
                              range(6)]
                    if pygame.draw.polygon(screen, (0, 0, 0, 0), points).collidepoint(event.pos):
                        shape.is_dragged = True
                        shape.offset_x = shape.x - event.pos[0]
                        shape.offset_y = shape.y - event.pos[1]
                        dragged_shape = shape
                        break
        elif event.type == pygame.MOUSEBUTTONUP:  # Отпускание кнопки мыши
            if dragged_shape:
                dragged_shape.is_dragged = False  # Завершаем перетаскивание
                # Перемещение перетаскиваемой фигуры в конец списка
                shapes.remove(dragged_shape)
                shapes.append(dragged_shape)
                dragged_shape = None  # Сброс перетаскиваемой фигуры
        elif event.type == pygame.MOUSEMOTION:  # Движение мыши
            if dragged_shape:  # Если фигура перетаскивается
                dragged_shape.x = event.pos[0] + dragged_shape.offset_x  # Обновляем координаты фигуры
                dragged_shape.y = event.pos[1] + dragged_shape.offset_y

    # Отрисовка всех фигур, кроме перетаскиваемой
    for shape in shapes:
        if not shape.is_dragged:
            shape.draw()

    # Отрисовка перетаскиваемой фигуры поверх остальных
    if dragged_shape:
        dragged_shape.draw()

    pygame.display.flip()  # Обновление экрана
    clock.tick(FPS)  # Ограничение частоты кадров

pygame.quit()  # Завершение работы Pygame
