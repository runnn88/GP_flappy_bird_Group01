import pygame
from src.core.scene_names import GAME_SCENE, SETTING_SCENE
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.utils.loader import load_font, load_image
from config import WIDTH

class MenuScene(BaseScene):
    def enter(self):
        self.background_1 = load_image("assets/images/backgrounds/night/1.png", (WIDTH, 600))
        self.background_2 = load_image("assets/images/backgrounds/night/2.png", (WIDTH, 600))
        self.background_3 = load_image("assets/images/backgrounds/night/3.png", (WIDTH, 600))
        self.background_4 = load_image("assets/images/backgrounds/night/4.png", (WIDTH, 600))

        self.game.audio.play_music("menu")
        self.font = load_font("PressStart2P-Regular.ttf", 50)
        self.body_font = load_font("VT323-Regular.ttf", 50)
        center_x = WIDTH // 2

        self.play_btn = Button(image=None, pos=(center_x, 300), font=self.body_font, 
                               base_color=(200,200,200), hovering_color=(0,255,0),
                               text_input="PLay Game", callback=self.start_game)
        self.setting_btn = Button(image=None, pos=(center_x, 400), font=self.body_font,
                                base_color=(200, 200, 200), hovering_color=(255, 255, 0),
                                text_input="Settings", callback=self.open_settings)

    def start_game(self):
        self.game.state_machine.change(GAME_SCENE)

    def open_settings(self):
        self.game.state_machine.change(SETTING_SCENE)
        
    def update(self, dt):
        self.play_btn.update(dt)
        self.setting_btn.update(dt)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.background_1, (0, 0))
        screen.blit(self.background_2, (0, 0))
        screen.blit(self.background_3, (0, 0))
        screen.blit(self.background_4, (0, 0))


        title = self.font.render("HUNGRY CHIKAWA", True, (255,255,255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 150)))
        
        self.play_btn.draw(screen)
        self.setting_btn.draw(screen)

    def handle_event(self, event):
        self.play_btn.handle_event(event)
        self.setting_btn.handle_event(event)
