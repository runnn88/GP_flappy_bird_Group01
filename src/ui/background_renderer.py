from src.utils.loader import load_image
from config import WIDTH, HEIGHT


class BackgroundRenderer:
    def __init__(self):
        self.fallback = load_image("assets/images/backgrounds/night/1.png", (WIDTH, HEIGHT))

    def draw(self, screen, parallax):
        if hasattr(parallax, "layers"):
            for layer in parallax.layers:
                screen.blit(layer.image, (layer.x, 0))
                screen.blit(layer.image, (layer.x + WIDTH, 0))
            return
        screen.blit(self.fallback, (0, 0))
