import pygame
from src.utils.loader import load_font

class HUD:
    def __init__(self):
        self.font = load_font("VT323", 36)

    def draw(self, screen, context):
        score_text = self.font.render(f"Score: {context.score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
