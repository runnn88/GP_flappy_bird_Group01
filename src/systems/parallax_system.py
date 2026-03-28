import pygame
from config import WIDTH, HEIGHT

class Layer:
    def __init__(self, speed):
        self.speed = speed
        self.x = 0
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill((50, 50, 50))

    def update(self, dt):
        self.x -= self.speed * dt
        if self.x <= -WIDTH:
            self.x = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, 0))
        screen.blit(self.image, (self.x + WIDTH, 0))


class ParallaxSystem:
    def __init__(self):
        self.layers = [
            Layer(30),
            Layer(80),
            Layer(200)
        ]

    def update(self, dt):
        for l in self.layers:
            l.update(dt)

    def draw(self, screen):
        for l in self.layers:
            l.draw(screen)