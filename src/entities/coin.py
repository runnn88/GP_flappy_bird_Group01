import pygame
from src.systems.animation_system import Animation
from src.utils.loader import load_image

def create_pixel_sprite(matrix, pixel_size, colors):
    surface = pygame.Surface(
        (len(matrix[0]) * pixel_size, len(matrix) * pixel_size),
        pygame.SRCALPHA
    )

    for y, row in enumerate(matrix):
        for x, pixel in enumerate(row):
            if pixel == 0:
                continue  # bỏ nền cho trong suốt
            pygame.draw.rect(
                surface,
                colors[pixel],
                (x * pixel_size, y * pixel_size, pixel_size, pixel_size)
            )

    return surface

APPLE_MATRIX = [
    [0,0,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [0,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,0,0],
    [0,0,0,3,0,0,0,0],
    [0,0,2,2,0,0,0,0],
]

APPLE_MATRIX_2 = [
    [0,0,1,1,1,1,0,0],
    [0,1,1,2,2,1,1,0],
    [1,1,2,1,1,2,1,1],
    [1,1,2,1,1,2,1,1],
    [0,1,1,2,2,1,1,0],
    [0,0,1,1,1,1,0,0],
    [0,0,0,3,0,0,0,0],
    [0,0,2,2,0,0,0,0],
]

APPLE_COLORS = {
    1: (255, 0, 0),      # đỏ
    2: (0, 200, 0),      # lá
    3: (139, 69, 19),    # cuống
}

class Coin:
    SIZE = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y

        frames = [
            create_pixel_sprite(APPLE_MATRIX, 4, APPLE_COLORS),
            create_pixel_sprite(APPLE_MATRIX_2, 4, APPLE_COLORS)
        ]

        self.animation = Animation(frames, fps=1)

    def update(self, dt, context):
        self.x -= context.scroll_speed * dt
        self.animation.update(dt)

    def draw(self, screen):
        frame = self.animation.get_frame()
        screen.blit(frame, (self.x, self.y))

    def rect(self):
        frame = self.animation.get_frame()
        return frame.get_rect(topleft=(self.x, self.y))

    def offscreen(self):
        frame = self.animation.get_frame()
        return self.x < -frame.get_width()

    
