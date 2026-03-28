import pygame
from config import WIDTH, HEIGHT
from src.utils.loader import load_image

class Layer:
    def __init__(self, speed):
        self.speed = speed
        self.x = 0
        self.image = load_image("assets/images/placeholder.png", (WIDTH, HEIGHT))

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

    def update(self, dt, context):
        for l in self.layers:
            layer_dt = dt * (context.scroll_speed / 200)
            l.update(layer_dt)
