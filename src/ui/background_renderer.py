from src.utils.loader import load_image
from config import WIDTH, HEIGHT


class BackgroundRenderer:
    def __init__(self):
        self.fallback = load_image("assets/images/backgrounds/night/1.png", (WIDTH, HEIGHT))

    def draw(self, screen, parallax):
        if hasattr(parallax, "layers"):
            
            if parallax.transition_progress < 1.0 and parallax.previous_layers:
                for layer in parallax.previous_layers:
                    layer.image.set_alpha(255)
                    screen.blit(layer.image, (layer.x, 0))
                    screen.blit(layer.image, (layer.x + WIDTH, 0))
                    
            alpha = int(parallax.transition_progress * 255)
            for layer in parallax.layers:
                layer.image.set_alpha(alpha)
                screen.blit(layer.image, (layer.x, 0))
                screen.blit(layer.image, (layer.x + WIDTH, 0))
            return
        screen.blit(self.fallback, (0, 0))
