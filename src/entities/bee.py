import pygame
import math
import random
from config import WIDTH

class Bee:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40 
        self.height = 40
        
        # try:
        self.image = pygame.image.load("assets/images/usagi.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # except FileNotFoundError:
        #     self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        #     pygame.draw.ellipse(self.image, (255, 200, 0), (0, 0, self.width, self.height))
        #     pygame.draw.ellipse(self.image, (0, 0, 0), (10, 10, 5, 5)) 
        
        self.speed = random.uniform(100, 200) 
        
        self.start_y = y
        self.time = random.uniform(0, 100) 
        self.amplitude = random.uniform(20, 50) 
        self.frequency = random.uniform(3, 6) 

    def update(self, dt, context):
        self.x -= (context.scroll_speed + self.speed) * dt
        
        self.time += dt
        self.y = self.start_y + math.sin(self.time * self.frequency) * self.amplitude

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def rect(self):
        hitbox_margin = 4
        return pygame.Rect(
            self.x + hitbox_margin, 
            self.y + hitbox_margin, 
            self.width - hitbox_margin * 2, 
            self.height - hitbox_margin * 2
        )

    def offscreen(self):
        return self.x < -self.width