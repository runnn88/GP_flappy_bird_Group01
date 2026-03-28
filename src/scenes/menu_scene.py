import pygame
from src.core.scene_names import GAME_SCENE
from src.scenes.base_scene import BaseScene

class MenuScene(BaseScene):
    def enter(self):
        self.font = pygame.font.SysFont(None, 60)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))

        title = self.font.render("INFINITE FLYER", True, (255,255,255))
        start = self.font.render("Press ENTER to Start", True, (200,200,200))

        screen.blit(title, (200, 200))
        screen.blit(start, (180, 300))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.state_machine.change(GAME_SCENE)
