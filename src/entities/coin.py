import pygame
from src.systems.animation_system import Animation
from src.utils.loader import load_image

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        frames = [
            load_image("assets/images/placeholder.png", (30, 30))
            for _ in range(2)
        ]

        self.animation = Animation(frames, fps=8)

    def update(self, dt, context):
        self.x -= context.scroll_speed * dt
        self.animation.update(dt)

    def rect(self):
        return pygame.Rect(self.x, self.y, 30, 30)

    def offscreen(self):
        return self.x < -30
