import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Класс мяча
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.speed_x = 4
        self.speed_y = -4

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.ellipse(screen, RED, self.rect)

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x *= -1

# Класс платформы
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 30, 100, 10)
        self.speed = 6

    def move(self, direction):
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed

        # Ограничение по краям экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

# Класс кирпича
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 75, 20)
        self.destroyed = False

    def draw(self, screen):
        if not self.destroyed:
            pygame.draw.rect(screen, GREEN, self.rect)

# Основной класс игры
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Arkanoid")
        self.clock = pygame.time.Clock()
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.paddle = Paddle()
        self.bricks = self.create_bricks()
        self.running = True

    def create_bricks(self):
        bricks = []
        for row in range(5):
            for col in range(10):
                brick = Brick(col * 80 + 10, row * 25 + 10)
                bricks.append(brick)
        return bricks

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move("left")
        if keys[pygame.K_RIGHT]:
            self.paddle.move("right")

        self.ball.move()

        # Отскок от стен
        if self.ball.rect.left <= 0 or self.ball.rect.right >= SCREEN_WIDTH:
            self.ball.speed_x *= -1
        if self.ball.rect.top <= 0:
            self.ball.speed_y *= -1

        # Падение шара
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.ball.reset()

        # Отскок от платформы
        if self.ball.rect.colliderect(self.paddle.rect) and self.ball.speed_y > 0:
            self.ball.speed_y *= -1

        # Отскок от кирпичей
        for brick in self.bricks:
            if not brick.destroyed and self.ball.rect.colliderect(brick.rect):
                brick.destroyed = True
                self.ball.speed_y *= -1

    def draw(self):
        self.screen.fill(BLACK)
        self.ball.draw(self.screen)
        self.paddle.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()