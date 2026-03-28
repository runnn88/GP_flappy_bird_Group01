import pygame
from config import SCROLL_SPEED

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, dt):
        self.x -= SCROLL_SPEED * dt

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 10)

    def rect(self):
        return pygame.Rect(self.x-10, self.y-10, 20, 20)

    def offscreen(self):
        return self.x < 0