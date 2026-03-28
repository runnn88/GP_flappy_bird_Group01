import pygame
import random
from config import WIDTH, HEIGHT, SCROLL_SPEED

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.width = 80
        self.gap = 150
        self.top = random.randint(50, HEIGHT - 200)

        self.gap_y = self.top + self.gap // 2

    def update(self, dt):
        self.x -= SCROLL_SPEED * dt

    def draw(self, screen):
        pygame.draw.rect(screen, (0,255,0), (self.x, 0, self.width, self.top))
        pygame.draw.rect(screen, (0,255,0),
                         (self.x, self.top + self.gap, self.width, HEIGHT))

    def offscreen(self):
        return self.x + self.width < 0

    def collides(self, rect):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top)
        bot_rect = pygame.Rect(self.x, self.top + self.gap, self.width, HEIGHT)
        return rect.colliderect(top_rect) or rect.colliderect(bot_rect)