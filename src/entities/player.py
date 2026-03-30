import pygame
from config import FLAP_FORCE
from src.systems.animation_system import Animation
from src.utils.loader import load_image

class Player:
    def __init__(self):
        self.x = 150
        self.y = 300
        self.vel = 0

        frames = [
            load_image("assets/images/usagi.png", (50, 35))
            for _ in range(3)
        ]

        self.animation = Animation(frames, fps=10)

    def update(self, dt, keys, context):
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.vel = FLAP_FORCE

        self.vel += context.gravity * dt
        self.y += self.vel * dt

        self.animation.update(dt)

    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 35)
