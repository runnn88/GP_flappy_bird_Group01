from config import HEIGHT
from src.utils.loader import load_image


class PipeRenderer:
    def __init__(self):
        self.image = load_image("assets/images/pipe-green.png", (80, HEIGHT))

    def draw(self, screen, pipes):
        for pipe in pipes:
            top_height = max(1, int(pipe.top))
            bottom_y = int(pipe.top + pipe.gap)
            bottom_height = max(1, HEIGHT - bottom_y)

            top_image = self.image.subsurface((0, 0, self.image.get_width(), top_height))
            bottom_image = self.image.subsurface((0, 0, self.image.get_width(), bottom_height))

            screen.blit(top_image, (pipe.x, 0))
            screen.blit(bottom_image, (pipe.x, bottom_y))
