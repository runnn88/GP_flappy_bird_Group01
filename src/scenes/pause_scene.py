import pygame
from src.core.scene_names import MENU_SCENE
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.utils.loader import load_font
from config import WIDTH, HEIGHT

class PauseScene(BaseScene):
    def __init__(self, game, previous_scene):
        super().__init__(game)
        self.previous_scene = previous_scene 

    def enter(self):
        self.title_font = load_font("PressStart2P-Regular.ttf", 60)
        self.btn_font = load_font("VT323-Regular.ttf", 48)
        
        self.buttons = []
        
        self.continue_btn = Button(
            image=None, pos=(300, 250), font=self.btn_font,
            base_color=(255, 246, 213), hovering_color=(255, 255, 255),
            text_input="Continue", callback=self.resume_game,
            bg_color=(132, 213, 242), border_radius=20, size=(220, 60)
        )
        self.buttons.append(self.continue_btn)

        self.menu_btn = Button(
            image=None, pos=(270, 350), font=self.btn_font,
            base_color=(255, 246, 213), hovering_color=(255, 255, 255),
            text_input="Back to Menu", callback=self.go_to_menu,
            bg_color=(249, 133, 183), border_radius=20, size=(280, 60)
        )
        self.buttons.append(self.menu_btn)

    def resume_game(self):
        self.game.state_machine.state = self.previous_scene

    def go_to_menu(self):
        self.game.state_machine.change(MENU_SCENE)

    def update(self, dt):
        for btn in self.buttons:
            btn.update(dt)

    def draw(self, screen):
        self.previous_scene.draw(screen)
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) 
        screen.blit(overlay, (0, 0))
        
        panel = pygame.Surface((520, 452), pygame.SRCALPHA)
        pygame.draw.rect(panel, (255, 242, 208, 200), panel.get_rect(), border_radius=25)
        screen.blit(panel, (140, 74))

        title = self.title_font.render("PAUSED", True, (182, 61, 169))
        screen.blit(title, title.get_rect(center=(420, 150)))

        for btn in self.buttons:
            btn.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.resume_game()
        
        for btn in self.buttons:
            btn.handle_event(event)