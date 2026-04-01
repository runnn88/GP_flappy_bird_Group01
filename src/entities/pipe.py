import math
import pygame
import random
from config import (
    HEIGHT,
    MAX_SCROLL_SPEED,
    PIPE_GAP_MAX,
    PIPE_GAP_MIN,
    PIPE_MOVE_AMPLITUDE,
    PIPE_MOVE_RISING_MULTIPLIER,
    PIPE_SPAWN_OFFSET,
    PIPE_MOVE_SPEED,
    SCROLL_SPEED,
    WIDTH,
)

class Pipe:
    def __init__(self):
        self.x = WIDTH + PIPE_SPAWN_OFFSET
        self.width = 80
        self.gap = random.randint(PIPE_GAP_MIN, PIPE_GAP_MAX)
        self.top = random.randint(50, HEIGHT - 200)
        self.base_top = float(self.top)
        self.vertical_phase = random.uniform(0, math.tau)
        self.vertical_speed = random.uniform(0.85, 1.15)
        self.gap_y = self.top + self.gap // 2

    def update(self, dt, context):
        self.x -= context.scroll_speed * dt
        if context.pipes_move_vertically:
            motion_speed = PIPE_MOVE_SPEED * self.vertical_speed
            if context.game_mode == "rising":
                speed_range = max(1, MAX_SCROLL_SPEED - SCROLL_SPEED)
                speed_progress = (context.scroll_speed - SCROLL_SPEED) / speed_range
                speed_progress = max(0, min(1, speed_progress))
                motion_speed *= 1 + ((PIPE_MOVE_RISING_MULTIPLIER - 1) * speed_progress)

            self.vertical_phase += motion_speed * dt
            offset = math.sin(self.vertical_phase) * PIPE_MOVE_AMPLITUDE
            min_top = 50
            max_top = HEIGHT - self.gap - 120
            self.top = max(min_top, min(max_top, self.base_top + offset))
        self.gap_y = self.top + (self.gap / 2)

    def offscreen(self):
        return self.x + self.width < 0

    def collides(self, rect):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top)
        bot_rect = pygame.Rect(self.x, self.top + self.gap, self.width, HEIGHT)
        return rect.colliderect(top_rect) or rect.colliderect(bot_rect)
