import pygame
from config import GRAVITY, FLAP_FORCE

class Player:
    def __init__(self):
        self.x = 150
        self.y = 300
        self.vel = 0

        self.frames = [pygame.Surface((50, 35)) for _ in range(3)]
        for f in self.frames:
            f.fill((255, 255, 0))

        self.frame = 0
        self.timer = 0

    def update(self, dt, keys):
        if keys[pygame.K_SPACE]:
            self.vel = FLAP_FORCE

        self.vel += GRAVITY * dt
        self.y += self.vel * dt

        # animation
        self.timer += dt
        if self.timer > 0.1:
            self.timer = 0
            self.frame = (self.frame + 1) % 3

    def draw(self, screen):
        screen.blit(self.frames[self.frame], (self.x, self.y))

    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 35)