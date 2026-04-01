import pygame
from config import FLAP_FORCE
from src.systems.animation_system import Animation
from src.utils.loader import load_image

class Player:
    def __init__(self):
        self.x = 150
        self.y = 300
        self.vel = 0

        # load ảnh gốc trước (không scale)
        original = pygame.image.load("assets/images/usa1.png").convert_alpha()

        target_width = 45  # bạn muốn rộng bao nhiêu thì chỉnh ở đây

        # giữ tỉ lệ
        ratio = target_width / original.get_width()
        target_height = int(original.get_height() * ratio)

        scaled = pygame.transform.scale(original, (target_width, target_height))

        frames = [scaled for _ in range(3)]

        self.animation = Animation(frames, fps=10)

        # lưu size thật để dùng rect
        self.width = target_width
        self.height = target_height

    def update(self, dt, keys, context):
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.vel = FLAP_FORCE

        self.vel += context.gravity * dt
        self.y += self.vel * dt

        self.animation.update(dt)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
