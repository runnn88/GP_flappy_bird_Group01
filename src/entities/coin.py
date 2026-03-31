import pygame
from config import PIPE_COIN_CLEARANCE
from src.systems.animation_system import Animation

class Coin:
    SIZE = 30

    def __init__(self, x, y, anchor_pipe=None):
        self.x = x
        self.y = y
        self.anchor_pipe = anchor_pipe

        frames = self._build_spin_frames()

        self.animation = Animation(frames, fps=10)
        self._sync_position()

    def update(self, dt, context):
        if self.anchor_pipe is not None:
            self._sync_position()
        else:
            self.x -= context.scroll_speed * dt
        self.animation.update(dt)

    def draw(self, screen):
        frame = self.animation.get_frame()
        screen.blit(frame, (self.x, self.y))

    def rect(self):
        frame = self.animation.get_frame()
        return frame.get_rect(topleft=(self.x, self.y))

    def offscreen(self):
        return self.x < -self.SIZE

    def _sync_position(self):
        if self.anchor_pipe is not None:
            self.x = self.anchor_pipe.x + ((self.anchor_pipe.width - self.SIZE) / 2)
            min_y = self.anchor_pipe.top + PIPE_COIN_CLEARANCE
            max_y = self.anchor_pipe.top + self.anchor_pipe.gap - self.SIZE - PIPE_COIN_CLEARANCE
            centered_y = self.anchor_pipe.top + ((self.anchor_pipe.gap - self.SIZE) / 2)
            self.y = max(min_y, min(max_y, centered_y))

    def _build_spin_frames(self):
        widths = [20, 14, 8, 14, 20, 24]
        return [self._build_frame(width) for width in widths]

    def _build_frame(self, body_width):
        frame = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
        center = self.SIZE // 2
        body_rect = pygame.Rect(0, 0, body_width, self.SIZE - 4)
        body_rect.center = (center, center)

        pygame.draw.ellipse(frame, (124, 74, 6), body_rect)
        inner_rect = body_rect.inflate(-4, -4)
        pygame.draw.ellipse(frame, (245, 204, 76), inner_rect)

        highlight_width = max(2, body_rect.width // 4)
        highlight_rect = pygame.Rect(0, 0, highlight_width, max(4, inner_rect.height - 4))
        highlight_rect.midleft = (inner_rect.left + 2, inner_rect.centery)
        pygame.draw.ellipse(frame, (255, 246, 180), highlight_rect)

        shine_rect = pygame.Rect(0, 0, max(2, body_rect.width // 5), max(2, body_rect.height // 5))
        shine_rect.center = (
            body_rect.centerx + max(1, body_rect.width // 6),
            body_rect.centery - max(2, body_rect.height // 4),
        )
        pygame.draw.ellipse(frame, (255, 255, 255, 120), shine_rect)

        return frame
