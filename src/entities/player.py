import pygame
import random

from config import FLAP_FORCE
from src.systems.animation_system import Animation
# from src.utils.loader import load_image

class Player:
    def __init__(self):
        self.x = 150
        self.y = 300
        self.vel = 0

        self.width = 45
        self.height = 35
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
        

        # frame = self.animation.get_frame()

        # # scale theo sin để giả vờ flap
        # import math
        # scale_y = 1 + 0.1 * math.sin(pygame.time.get_ticks() * 0.02)

        # new_height = int(frame.get_height() * scale_y)
        # scaled = pygame.transform.scale(frame, (frame.get_width(), new_height))

        self.trail = []
        self.max_trail_length = 30

        self.particles = []

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

        if not self.trail or abs(self.y - self.trail[-1]["pos"][1]) > 2:
            self.trail.append({
                "pos": (self.x, self.y + self.height // 2),
                "life": 1.0
            })

        # ===== fade trail =====
        for p in self.trail:
            p["life"] -= dt * 1.8   # tăng lên cho fade nhanh hơn

        # ===== xoá điểm chết =====
        self.trail = [p for p in self.trail if p["life"] > 0]

        # ===== giới hạn length =====
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

        # ===== MOVE TRAIL THEO SCROLL =====
        for p in self.trail:
            p["pos"] = (
                p["pos"][0] - context.scroll_speed * dt,
                p["pos"][1]
            )

        if len(self.trail) >= 2:
            last = self.trail[-1]["pos"]
            new = (self.x, self.y + self.height // 2)

            mid = (
                (last[0] + new[0]) / 2,
                (last[1] + new[1]) / 2
            )

            self.trail.append({"pos": mid, "life": 1.0})

        # ===== SPAWN PARTICLE =====
        for _ in range(1):  # số lượng mỗi frame
            self.particles.append({
                "pos": [self.x, self.y + self.height // 2],

                # bay ngược + hơi random
                "vel": [
                    random.uniform(-30, -80),   # bay về bên trái
                    random.uniform(-30, 30)     # bay lên/xuống nhẹ
                ],

                "life": 1.2,
                "size": random.randint(3, 6),
                "color": random.choice([
                    (255, 255, 255),
                    (255, 255, 120),
                    (120, 255, 255),
                    (255, 150, 255),
                ]),
                "angle": random.uniform(0, 360),
                "spin": random.uniform(-180, 180)  # độ quay mỗi giây
            })

        # ===== UPDATE PARTICLES =====
        for p in self.particles:
            p["life"] -= dt * 2
            p["pos"][0] += p["vel"][0] * dt
            p["pos"][1] += p["vel"][1] * dt

            # gravity nhẹ
            p["vel"][1] += 50 * dt

            # scroll theo map
            p["pos"][0] -= context.scroll_speed * dt

            # xoay
            p["angle"] += p["spin"] * dt

            # x, y = p["pos"]
            # vx, vy = p["vel"]

            # # di chuyển
            # x += vx * dt
            # y += vy * dt

            # # gravity nhẹ cho particle
            # vy += 200 * dt

            # # scroll theo map
            # x -= context.scroll_speed * dt

            # p["pos"] = (x, y)
            # p["vel"] = (vx, vy)

            # # fade
            # p["life"] -= dt * 1.5

        # xoá particle chết
        self.particles = [p for p in self.particles if p["life"] > 0]  
        self.particles = self.particles[-200:]  
        
        # if len(self.trail) > self.max_trail_length:
        #     self.trail.pop(0)

        # # giảm life theo thời gian
        # for p in self.trail:
        #     p["life"] -= dt * 1.5  # tốc độ fade

        # # xoá particle đã hết
        # self.trail = [p for p in self.trail if p["life"] > 0]

        # self.trail = self.trail[-40:]

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
