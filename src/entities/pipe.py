import pygame
import random
from config import HEIGHT, PIPE_GAP_MAX, PIPE_GAP_MIN, WIDTH

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.width = 80
        self.gap = random.randint(PIPE_GAP_MIN, PIPE_GAP_MAX)
        self.top = random.randint(50, HEIGHT - 200)
        self.gap_y = self.top + self.gap // 2

    def update(self, dt, context):
        self.x -= context.scroll_speed * dt

    def offscreen(self):
        return self.x + self.width < 0

    def collides(self, rect):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top)
        bot_rect = pygame.Rect(self.x, self.top + self.gap, self.width, HEIGHT)
        return rect.colliderect(top_rect) or rect.colliderect(bot_rect)
