import pygame
from config import FLAP_FORCE
from src.systems.animation_system import Animation
# from src.utils.loader import load_image

class Player:
    def __init__(self):
        self.x = 150
        self.y = 300
        self.vel = 0

        self.width = 50
        self.height = 50
        sheet = pygame.image.load("assets/images/fat_bird.png")
        frame_count = 5
        frame_w = sheet.get_width() // frame_count
        frame_h = sheet.get_height()
        
        self.frames = []
        for i in range(frame_count):
            rect = pygame.Rect(i * frame_w, 0, frame_w, frame_h)
            image = sheet.subsurface(rect)
            image = pygame.transform.scale(image, (self.width, self.height))
            self.frames.append(image)

        self.idle_anim = Animation([self.frames[0]], fps=1)
        self.flap_anim = Animation(self.frames, fps=15)

        self.animation = self.idle_anim
        

    def update(self, dt, keys, context):
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.vel = FLAP_FORCE

        self.vel += context.gravity * dt
        self.y += self.vel * dt
        
        if self.vel < 0: #flapping
            self.animation = self.flap_anim
        else: 
            self.animation = self.idle_anim

        self.animation.update(dt)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
