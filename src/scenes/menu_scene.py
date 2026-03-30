import pygame
from src.core.scene_names import GAME_SCENE
from src.scenes.base_scene import BaseScene

class MenuScene(BaseScene):
    def enter(self):
        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 32)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))

        title = self.font.render("INFINITE FLYER", True, (255,255,255))
        start = self.font.render("Press ENTER to Start", True, (200,200,200))
        mode = self.small_font.render(
            f"Mode: {self.game.context.game_mode}  (1 = Rising Speed, 2 = Steady Speed)",
            True,
            (220, 220, 220),
        )

        screen.blit(title, (200, 200))
        screen.blit(start, (180, 300))
        screen.blit(mode, (120, 380))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.game.context.game_mode = "rising"
            if event.key == pygame.K_2:
                self.game.context.game_mode = "steady"
            if event.key == pygame.K_RETURN:
                self.game.state_machine.change(GAME_SCENE)
