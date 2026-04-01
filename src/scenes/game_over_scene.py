import pygame
from src.core.scene_names import GAME_SCENE, MENU_SCENE
from src.scenes.base_scene import BaseScene
from src.utils.loader import load_font

class GameOverScene(BaseScene):
    def enter(self):
        self.font = load_font("VT323-Regular.ttf", 60) 

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))

        over = self.font.render("GAME OVER", True, (255,0,0))
        score = self.font.render(f"Score: {self.game.context.score}", True, (255,255,255))
        retry = self.font.render("Press R to Retry", True, (200,200,200))
        menu = self.font.render("Press ESC for Menu", True, (200,200,200))

        screen.blit(over, (250, 180))
        screen.blit(score, (300, 260))
        screen.blit(retry, (230, 340))
        screen.blit(menu, (210, 420))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.game.state_machine.change(GAME_SCENE)

            if event.key == pygame.K_ESCAPE:
                self.game.state_machine.change(MENU_SCENE)
