from pathlib import Path

import pygame
from config import WIDTH, HEIGHT
from src.utils.loader import load_image


LAYER_SPEEDS = [2, 12, 50, 140]
BACKGROUND_ASSET_ROOT = Path("assets/images/backgrounds")
BACKGROUND_THEME_FALLBACKS = {
    "night": "night",
    "noon": "noon",
    "sunrise": "sunrise",
    "sunset": "sunset",
}

class Layer:
    def __init__(self, image_path, speed):
        self.speed = speed
        self.x = 0
        self.image = load_image(image_path, (WIDTH, HEIGHT))

    def update(self, dt):
        self.x -= self.speed * dt
        if self.x <= -WIDTH:
            self.x = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, 0))
        screen.blit(self.image, (self.x + WIDTH, 0))


class ParallaxSystem:
    def __init__(self, initial_theme="noon"):
        self.current_theme = None
        self.layers = []
        self.set_theme(initial_theme)

    def set_theme(self, theme_name):
        resolved_theme = self._resolve_theme(theme_name)
        if resolved_theme == self.current_theme:
            return

        self.current_theme = resolved_theme
        self.layers = [
            Layer(str(BACKGROUND_ASSET_ROOT / resolved_theme / f"{index}.png"), speed)
            for index, speed in enumerate(LAYER_SPEEDS, start=1)
        ]

    def _resolve_theme(self, theme_name):
        candidate_dir = BACKGROUND_ASSET_ROOT / theme_name
        if self._has_complete_theme(candidate_dir):
            return theme_name

        fallback_theme = BACKGROUND_THEME_FALLBACKS.get(theme_name, "night")
        fallback_dir = BACKGROUND_ASSET_ROOT / fallback_theme
        if self._has_complete_theme(fallback_dir):
            return fallback_theme
        return "night"

    def _has_complete_theme(self, theme_dir):
        return all((theme_dir / f"{index}.png").exists() for index in range(1, 5))

    def update(self, dt, context):
        self.set_theme(context.background_theme)
        for l in self.layers:
            layer_dt = dt * (context.scroll_speed / 200)
            l.update(layer_dt)
