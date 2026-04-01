import pygame

from config import PIPE_COIN_CLEARANCE
from src.systems.animation_system import Animation


def create_pixel_sprite(matrix, pixel_size, colors):
    surface = pygame.Surface(
        (len(matrix[0]) * pixel_size, len(matrix) * pixel_size),
        pygame.SRCALPHA,
    )

    for y, row in enumerate(matrix):
        for x, pixel in enumerate(row):
            if pixel == 0:
                continue
            pygame.draw.rect(
                surface,
                colors[pixel],
                (x * pixel_size, y * pixel_size, pixel_size, pixel_size),
            )

    return surface


APPLE_MATRIX = [
    [0, 0, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 4, 1, 0],
    [1, 1, 1, 1, 1, 1, 4, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
]

APPLE_COLORS = {
    1: (255, 0, 0),
    2: (0, 200, 0),
    3: (139, 69, 19),
    4: (255, 255, 255),
}


class Coin:
    SIZE = 32
    _cached_frames = None

    def __init__(self, x, y, anchor_pipe=None):
        self.x = x
        self.y = y
        self.anchor_pipe = anchor_pipe

        if Coin._cached_frames is None:
            Coin._cached_frames = self._build_frames()

        self.animation = Animation(Coin._cached_frames, fps=12)
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

    def _build_frames(self):
        base = create_pixel_sprite(APPLE_MATRIX, 4, APPLE_COLORS)
        base = pygame.transform.scale(base, (self.SIZE, self.SIZE))

        glow = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (255, 80, 80, 80), (0, 0, self.SIZE, self.SIZE))

        widths = [32, 26, 20, 14, 20, 26, 32]
        frames = []
        for width in widths:
            frame = glow.copy()
            scaled = pygame.transform.scale(base, (width, self.SIZE))
            rect = scaled.get_rect(center=(self.SIZE // 2, self.SIZE // 2))
            frame.blit(scaled, rect)
            frames.append(frame)

        return frames
