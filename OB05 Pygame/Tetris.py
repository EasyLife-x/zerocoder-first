import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 200

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
DARK_GRAY = (30, 30, 30)
GRID_COLOR = (50, 50, 50)
RED = (255, 50, 50)
GREEN = (50, 255, 100)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 50)
PURPLE = (200, 50, 255)
CYAN = (50, 220, 255)
ORANGE = (255, 150, 50)

# Цвета с 3D эффектом (основной цвет, цвет тени)
COLORS_3D = [
    (RED, (200, 30, 30)),  # Красный
    (GREEN, (30, 200, 60)),  # Зеленый
    (BLUE, (30, 100, 200)),  # Синий
    (YELLOW, (200, 200, 30)),  # Желтый
    (PURPLE, (150, 30, 200)),  # Фиолетовый
    (CYAN, (30, 180, 200)),  # Голубой
    (ORANGE, (200, 100, 30))  # Оранжевый
]

# Формы тетрамино
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]  # Z
]


class Tetromino:
    """Класс для представления тетрамино"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx]
        self.color = COLORS_3D[self.shape_idx]
        self.rotation = 0

    def rotate(self):
        """Поворот фигуры на 90 градусов"""
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]

        for r in range(rows):
            for c in range(cols):
                rotated[c][rows - 1 - r] = self.shape[r][c]

        return rotated

    def get_positions(self):
        """Получение всех позиций ячеек фигуры"""
        positions = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    positions.append((self.x + x, self.y + y))
        return positions


class TetrisGame:
    """Основной класс игры Тетрис"""

    def __init__(self):
        # Получаем размеры экрана для динамического масштабирования
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h

        # Создаем окно с возможностью изменения размера
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Тетрис")
        self.clock = pygame.time.Clock()

        # Шрифты для текста
        self.font = pygame.font.SysFont(None, int(self.screen_height * 0.033))
        self.small_font = pygame.font.SysFont(None, int(self.screen_height * 0.026))
        self.large_font = pygame.font.SysFont(None, int(self.screen_height * 0.067))

        # Инициализация игры
        self.reset_game()
        self.game_state = "menu"  # menu, playing, paused, game_over
        self.next_piece = self.new_piece()

        # Переменные для масштабирования
        self.scale_factor = 1.0
        self.play_area_x = 0
        self.play_area_y = 0
        self.sidebar_x = 0
        self.grid_size = 30

    def reset_game(self):
        """Сброс игры к начальному состоянию"""
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = 0.5  # секунды на падение
        self.fall_time = 0
        self.paused = False

    def new_piece(self):
        """Создание новой фигуры"""
        return Tetromino(GRID_WIDTH // 2 - 1, 0)

    def valid_position(self, piece=None):
        """Проверка, является ли позиция фигуры допустимой"""
        if piece is None:
            piece = self.current_piece

        for x, y in piece.get_positions():
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return False
            if y >= 0 and self.grid[y][x]:
                return False
        return True

    def merge_piece(self):
        """Объединение фигуры с игровым полем"""
        for x, y in self.current_piece.get_positions():
            if y >= 0:
                self.grid[y][x] = self.current_piece.color

    def clear_lines(self):
        """Очистка заполненных линий"""
        lines_to_clear = []
        for i, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                lines_to_clear.append(i)

        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])

        # Обновление счета
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            # Начисление очков: 1 линия - 100, 2 линии - 300, 3 линии - 500, 4 линии - 800
            self.score += [100, 300, 500, 800][min(len(lines_to_clear) - 1, 3)] * self.level
            # Увеличение уровня каждые 10 очищенных линий
            self.level = self.lines_cleared // 10 + 1
            # Увеличение скорости падения с каждым уровнем
            self.fall_speed = max(0.05, 0.5 - (self.level - 1) * 0.05)

    def move(self, dx, dy):
        """Перемещение текущей фигуры"""
        self.current_piece.x += dx
        self.current_piece.y += dy
        if not self.valid_position():
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            if dy > 0:  # Если падение вниз
                self.merge_piece()
                self.clear_lines()
                self.current_piece = self.next_piece
                self.next_piece = self.new_piece()
                if not self.valid_position():
                    self.game_state = "game_over"

    def rotate_piece(self):
        """Поворот текущей фигуры"""
        original_shape = self.current_piece.shape
        self.current_piece.shape = self.current_piece.rotate()
        if not self.valid_position():
            self.current_piece.shape = original_shape

    def hard_drop(self):
        """Мгновенное падение фигуры вниз"""
        while self.valid_position():
            self.current_piece.y += 1
        self.current_piece.y -= 1
        self.merge_piece()
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if not self.valid_position():
            self.game_state = "game_over"

    def calculate_dimensions(self):
        """Пересчет размеров элементов для заполнения всего экрана по высоте"""
        # Вычисляем размер ячейки, чтобы игровое поле заполнило всю высоту экрана
        self.grid_size = self.screen_height // GRID_HEIGHT

        # Размеры игрового поля
        self.play_area_width = GRID_WIDTH * self.grid_size
        self.play_area_height = GRID_HEIGHT * self.grid_size

        # Позиции элементов (центрируем по горизонтали)
        self.play_area_x = (self.screen_width - SIDEBAR_WIDTH - self.play_area_width) // 2
        self.play_area_y = 0  # Начинаем с верха экрана
        self.sidebar_x = self.play_area_x + self.play_area_width

    def draw_grid(self):
        """Отрисовка игрового поля"""
        # Отрисовка фона игрового поля
        pygame.draw.rect(self.screen, DARK_GRAY,
                         (self.play_area_x - int(5 * self.scale_factor),
                          self.play_area_y - int(5 * self.scale_factor),
                          self.play_area_width + int(10 * self.scale_factor),
                          self.play_area_height + int(10 * self.scale_factor)))

        # Отрисовка сетки
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pygame.draw.rect(self.screen, GRID_COLOR,
                                 (self.play_area_x + x * self.grid_size,
                                  self.play_area_y + y * self.grid_size,
                                  self.grid_size, self.grid_size), 1)

                # Отрисовка заполненных ячеек
                if self.grid[y][x]:
                    color, shadow = self.grid[y][x]
                    rect = pygame.Rect(self.play_area_x + x * self.grid_size,
                                       self.play_area_y + y * self.grid_size,
                                       self.grid_size, self.grid_size)
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, shadow, rect, max(1, int(2 * self.scale_factor)))

    def draw_current_piece(self):
        """Отрисовка текущей фигуры"""
        if self.game_state == "playing" or self.game_state == "paused":
            for x, y in self.current_piece.get_positions():
                if y >= 0:
                    color, shadow = self.current_piece.color
                    rect = pygame.Rect(self.play_area_x + x * self.grid_size,
                                       self.play_area_y + y * self.grid_size,
                                       self.grid_size, self.grid_size)
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, shadow, rect, max(1, int(2 * self.scale_factor)))

    def draw_next_piece(self):
        """Отрисовка следующей фигуры в сайдбаре"""
        # Отрисовка фона для следующей фигуры
        next_piece_height = int(self.screen_height * 0.2)
        pygame.draw.rect(self.screen, DARK_GRAY,
                         (self.sidebar_x + 10, 20,
                          SIDEBAR_WIDTH - 20, next_piece_height))
        pygame.draw.rect(self.screen, GRAY,
                         (self.sidebar_x + 10, 20,
                          SIDEBAR_WIDTH - 20, next_piece_height), 2)

        # Заголовок
        next_text = self.font.render("Следующая:", True, WHITE)
        self.screen.blit(next_text, (self.sidebar_x + 20, 40))

        # Отрисовка следующей фигуры
        shape = self.next_piece.shape
        color, shadow = self.next_piece.color

        # Центрируем фигуру в области
        piece_width = len(shape[0]) * self.grid_size
        piece_height = len(shape) * self.grid_size
        start_x = self.sidebar_x + 20 + (SIDEBAR_WIDTH - 40 - piece_width) // 2
        start_y = 80 + (next_piece_height - 100 - piece_height) // 2

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(start_x + x * self.grid_size,
                                       start_y + y * self.grid_size,
                                       self.grid_size, self.grid_size)
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, shadow, rect, max(1, int(2 * self.scale_factor)))

    def draw_sidebar(self):
        """Отрисовка сайдбара с информацией"""
        # Отрисовка сайдбара (занимает оставшееся пространство по высоте)
        sidebar_top = int(self.screen_height * 0.25)
        sidebar_height = self.screen_height - sidebar_top - 20

        pygame.draw.rect(self.screen, DARK_GRAY,
                         (self.sidebar_x + 10, sidebar_top,
                          SIDEBAR_WIDTH - 20, sidebar_height))
        pygame.draw.rect(self.screen, GRAY,
                         (self.sidebar_x + 10, sidebar_top,
                          SIDEBAR_WIDTH - 20, sidebar_height), 2)

        # Счет
        score_text = self.font.render(f"Счет: {self.score}", True, WHITE)
        self.screen.blit(score_text, (self.sidebar_x + 20, sidebar_top + 20))

        # Уровень
        level_text = self.font.render(f"Уровень: {self.level}", True, WHITE)
        self.screen.blit(level_text, (self.sidebar_x + 20, sidebar_top + 70))

        # Линии
        lines_text = self.font.render(f"Линии: {self.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (self.sidebar_x + 20, sidebar_top + 120))

        # Управление
        controls_y = sidebar_top + 180
        controls = [
            "Управление:",
            "A - Влево",
            "D - Вправо",
            "S - Вниз",
            "W - Поворот",
            "Пробел - Сброс",
            "ESC - Меню"
        ]

        for i, text in enumerate(controls):
            ctrl_text = self.small_font.render(text, True, WHITE)
            self.screen.blit(ctrl_text, (self.sidebar_x + 20, controls_y + i * 35))

    def draw_menu(self):
        """Отрисовка главного меню"""
        # Затемнение фона
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Заголовок
        title = self.large_font.render("ТЕТРИС", True, CYAN)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        self.screen.blit(title, title_rect)

        # Кнопки
        button_width = 300
        button_height = 60
        button_y_start = self.screen_height // 2

        # Кнопка "Играть"
        play_button = pygame.Rect(self.screen_width // 2 - button_width // 2,
                                  button_y_start, button_width, button_height)
        pygame.draw.rect(self.screen, GREEN, play_button, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, play_button, 3, border_radius=10)
        play_text = self.font.render("ИГРАТЬ", True, BLACK)
        play_text_rect = play_text.get_rect(center=play_button.center)
        self.screen.blit(play_text, play_text_rect)

        # Кнопка "Закрыть"
        quit_button = pygame.Rect(self.screen_width // 2 - button_width // 2,
                                  button_y_start + 100, button_width, button_height)
        pygame.draw.rect(self.screen, RED, quit_button, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, quit_button, 3, border_radius=10)
        quit_text = self.font.render("ЗАКРЫТЬ", True, WHITE)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        self.screen.blit(quit_text, quit_text_rect)

        return play_button, quit_button

    def draw_pause_menu(self):
        """Отрисовка меню паузы"""
        # Затемнение фона
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Пауза
        pause_text = self.large_font.render("ПАУЗА", True, YELLOW)
        pause_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        self.screen.blit(pause_text, pause_rect)

        # Кнопки
        button_width = 300
        button_height = 60
        button_y_start = self.screen_height // 2

        # Кнопка "Продолжить"
        resume_button = pygame.Rect(self.screen_width // 2 - button_width // 2,
                                    button_y_start, button_width, button_height)
        pygame.draw.rect(self.screen, GREEN, resume_button, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, resume_button, 3, border_radius=10)
        resume_text = self.font.render("ПРОДОЛЖИТЬ", True, BLACK)
        resume_text_rect = resume_text.get_rect(center=resume_button.center)
        self.screen.blit(resume_text, resume_text_rect)

        # Кнопка "Выйти в меню"
        menu_button = pygame.Rect(self.screen_width // 2 - button_width // 2,
                                  button_y_start + 100, button_width, button_height)
        pygame.draw.rect(self.screen, BLUE, menu_button, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, menu_button, 3, border_radius=10)
        menu_text = self.font.render("В МЕНЮ", True, WHITE)
        menu_text_rect = menu_text.get_rect(center=menu_button.center)
        self.screen.blit(menu_text, menu_text_rect)

        return resume_button, menu_button

    def draw_game_over(self):
        """Отрисовка экрана окончания игры"""
        # Затемнение фона
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Игра окончена
        game_over_text = self.large_font.render("ИГРА ОКОНЧЕНА", True, RED)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        self.screen.blit(game_over_text, game_over_rect)

        # Счет
        score_text = self.font.render(f"Счет: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(score_text, score_rect)

        # Кнопки
        button_width = 300
        button_height = 60
        button_y_start = self.screen_height // 2 + 100

        # Кнопка "Играть снова"
        restart_button = pygame.Rect(self.screen_width // 2 - button_width // 2,
                                     button_y_start, button_width, button_height)
        pygame.draw.rect(self.screen, GREEN, restart_button, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, restart_button, 3, border_radius=10)
        restart_text = self.font.render("ИГРАТЬ СНОВА", True, BLACK)
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        self.screen.blit(restart_text, restart_text_rect)

        # Кнопка "В меню"
        menu_button = pygame.Rect(self.screen_width // 2 - button_width // 2,
                                  button_y_start + 100, button_width, button_height)
        pygame.draw.rect(self.screen, BLUE, menu_button, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, menu_button, 3, border_radius=10)
        menu_text = self.font.render("В МЕНЮ", True, WHITE)
        menu_text_rect = menu_text.get_rect(center=menu_button.center)
        self.screen.blit(menu_text, menu_text_rect)

        return restart_button, menu_button

    def handle_menu_events(self, play_button, quit_button):
        """Обработка событий в главном меню"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    if play_button.collidepoint(event.pos):
                        self.game_state = "playing"
                        self.reset_game()
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            if event.type == pygame.VIDEORESIZE:
                # Обработка изменения размера окна
                self.screen_width, self.screen_height = event.size
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                self.calculate_dimensions()
                self.font = pygame.font.SysFont(None, max(12, int(self.screen_height * 0.033)))
                self.small_font = pygame.font.SysFont(None, max(10, int(self.screen_height * 0.026)))
                self.large_font = pygame.font.SysFont(None, max(24, int(self.screen_height * 0.067)))

    def handle_game_events(self):
        """Обработка игровых событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # При нажатии ESC переходим в меню паузы
                    self.game_state = "paused"

                if self.game_state == "playing":
                    if event.key == pygame.K_a:
                        self.move(-1, 0)
                    elif event.key == pygame.K_d:
                        self.move(1, 0)
                    elif event.key == pygame.K_s:
                        self.move(0, 1)
                    elif event.key == pygame.K_w:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()

            if event.type == pygame.VIDEORESIZE:
                # Обработка изменения размера окна
                self.screen_width, self.screen_height = event.size
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                self.calculate_dimensions()
                self.font = pygame.font.SysFont(None, max(12, int(self.screen_height * 0.033)))
                self.small_font = pygame.font.SysFont(None, max(10, int(self.screen_height * 0.026)))
                self.large_font = pygame.font.SysFont(None, max(24, int(self.screen_height * 0.067)))

    def handle_pause_events(self, resume_button, menu_button):
        """Обработка событий в меню паузы"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # При нажатии ESC возвращаемся к игре
                    self.game_state = "playing"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    if resume_button.collidepoint(event.pos):
                        self.game_state = "playing"
                    elif menu_button.collidepoint(event.pos):
                        self.game_state = "menu"

            if event.type == pygame.VIDEORESIZE:
                # Обработка изменения размера окна
                self.screen_width, self.screen_height = event.size
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                self.calculate_dimensions()
                self.font = pygame.font.SysFont(None, max(12, int(self.screen_height * 0.033)))
                self.small_font = pygame.font.SysFont(None, max(10, int(self.screen_height * 0.026)))
                self.large_font = pygame.font.SysFont(None, max(24, int(self.screen_height * 0.067)))

    def handle_game_over_events(self, restart_button, menu_button):
        """Обработка событий на экране окончания игры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    if restart_button.collidepoint(event.pos):
                        self.game_state = "playing"
                        self.reset_game()
                    elif menu_button.collidepoint(event.pos):
                        self.game_state = "menu"

            if event.type == pygame.VIDEORESIZE:
                # Обработка изменения размера окна
                self.screen_width, self.screen_height = event.size
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                self.calculate_dimensions()
                self.font = pygame.font.SysFont(None, max(12, int(self.screen_height * 0.033)))
                self.small_font = pygame.font.SysFont(None, max(10, int(self.screen_height * 0.026)))
                self.large_font = pygame.font.SysFont(None, max(24, int(self.screen_height * 0.067)))

    def update(self):
        """Обновление игровой логики"""
        if self.game_state == "playing":
            self.fall_time += self.clock.get_time() / 1000
            if self.fall_time >= self.fall_speed:
                self.move(0, 1)
                self.fall_time = 0

    def draw(self):
        """Отрисовка всего экрана"""
        self.screen.fill(BLACK)

        if self.game_state == "menu":
            play_button, quit_button = self.draw_menu()
            pygame.display.flip()
            self.handle_menu_events(play_button, quit_button)

        elif self.game_state == "playing":
            self.draw_grid()
            self.draw_current_piece()
            self.draw_next_piece()
            self.draw_sidebar()
            pygame.display.flip()

        elif self.game_state == "paused":
            self.draw_grid()
            self.draw_current_piece()
            self.draw_next_piece()
            self.draw_sidebar()
            resume_button, menu_button = self.draw_pause_menu()
            pygame.display.flip()
            self.handle_pause_events(resume_button, menu_button)

        elif self.game_state == "game_over":
            self.draw_grid()
            self.draw_current_piece()
            self.draw_next_piece()
            self.draw_sidebar()
            restart_button, menu_button = self.draw_game_over()
            pygame.display.flip()
            self.handle_game_over_events(restart_button, menu_button)

    def run(self):
        """Основной игровой цикл"""
        while True:
            # Пересчитываем размеры при каждом кадре
            self.calculate_dimensions()
            self.handle_game_events()
            self.update()
            self.draw()
            self.clock.tick(60)


# Запуск игры
if __name__ == "__main__":
    game = TetrisGame()
    game.run()