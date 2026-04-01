from pathlib import Path

import pygame
from config import WIDTH, HEIGHT
from src.utils.loader import load_image


DEFAULT_LAYER_SPEEDS = [2, 12, 50, 140]
BACKGROUND_ASSET_ROOT = Path("assets/images/backgrounds")
BACKGROUND_THEME_FALLBACKS = {
    "flipped": "flipped",
    "night": "night",
    "noon": "noon",
    "sunrise": "sunrise",
    "sunset": "sunset",
}
THEME_LAYER_CONFIGS = {
    "flipped": [
        {"speed": 2, "repeat": True, "centered": False},
        {"speed": 0, "repeat": False, "centered": True},
        {"speed": 12, "repeat": True, "centered": False},
    ],
}

class Layer:
    def __init__(self, image_path, speed, repeat=True, centered=False):
        self.speed = speed
        self.repeat = repeat
        self.centered = centered
        self.x = 0
        self.image = load_image(image_path, (WIDTH, HEIGHT))

    def update(self, dt):
        if not self.repeat or self.speed == 0:
            return
        self.x -= self.speed * dt
        if self.x <= -WIDTH:
            self.x = 0

    def draw(self, screen):
        if self.centered:
            screen.blit(self.image, (0, 0))
            return

        if not self.repeat:
            screen.blit(self.image, (self.x, 0))
            return

        screen.blit(self.image, (self.x, 0))
        screen.blit(self.image, (self.x + WIDTH, 0))


class ParallaxSystem:
    def __init__(self, initial_theme="noon"):
        self.current_theme = None
        self.layers = []
        
        self.previous_layers = []
        self.transition_progress = 1.0 
        self.transition_duration = 2.0
        
        self.set_theme(initial_theme)

    def set_theme(self, theme_name):
        resolved_theme = self._resolve_theme(theme_name)
        if resolved_theme == self.current_theme:
            return
        
        if self.layers: 
            self.previous_layers = self.layers
            self.transition_progress = 0.0
        else: 
            self.transition_progress = 1.0 

        self.current_theme = resolved_theme
        image_paths = self._get_theme_image_paths(resolved_theme)
        layer_configs = self._get_layer_configs(resolved_theme, len(image_paths))
        self.layers = [
            Layer(
                str(image_path),
                layer_config["speed"],
                repeat=layer_config["repeat"],
                centered=layer_config["centered"],
            )
            for image_path, layer_config in zip(image_paths, layer_configs)
        ]
        
        if self.previous_layers:
            for new_layer, old_layer in zip(self.layers, self.previous_layers):
                new_layer.x = old_layer.x

    def _resolve_theme(self, theme_name):
        candidate_dir = BACKGROUND_ASSET_ROOT / theme_name
        if self._has_theme_assets(candidate_dir):
            return theme_name

        fallback_theme = BACKGROUND_THEME_FALLBACKS.get(theme_name, "night")
        fallback_dir = BACKGROUND_ASSET_ROOT / fallback_theme
        if self._has_theme_assets(fallback_dir):
            return fallback_theme
        return "night"

    def _has_theme_assets(self, theme_dir):
        return any(theme_dir.glob("*.png"))

    def _get_theme_image_paths(self, theme_name):
        theme_dir = BACKGROUND_ASSET_ROOT / theme_name
        return sorted(theme_dir.glob("*.png"))

    def _get_layer_configs(self, theme_name, layer_count):
        theme_config = THEME_LAYER_CONFIGS.get(theme_name)
        if theme_config is not None:
            return theme_config[:layer_count]

        return [
            {"speed": speed, "repeat": True, "centered": False}
            for speed in DEFAULT_LAYER_SPEEDS[:layer_count]
        ]

    def update(self, dt, context):
        self.set_theme(context.background_theme)
        
        if self.transition_progress < 1.0:
            self.transition_progress = min(1.0, self.transition_progress + (dt / self.transition_duration))
        
        layer_dt = dt * (context.scroll_speed / 200)
        
        for l in self.layers:
            l.update(layer_dt)
        for l in self.previous_layers:
            l.update(layer_dt)
