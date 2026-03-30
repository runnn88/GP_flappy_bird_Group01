import pygame
from src.core.scene_names import MENU_SCENE
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from config import WIDTH 

class SettingScene(BaseScene):
    def enter(self):
        self.font = pygame.font.SysFont(None, 48)
        self.title_font = pygame.font.SysFont(None, 64)
        
        self.themes = ["noon", "sunset", "night", "sunrise"]
        self.buttons = []
        center_x = WIDTH // 2

        mode_text = "Mode: Endless Rush" if self.game.context.is_speed_increasing else "Mode: Normal"
        self.mode_btn = Button(
            image=None, pos=(center_x, 200), font=self.font,
            base_color=(200, 200, 200), hovering_color=(255, 255, 0),
            text_input=mode_text, callback=self.toggle_mode
        )
        self.buttons.append(self.mode_btn)

        theme_text = f"Theme: {self.game.context.background_theme.capitalize()}"
        self.theme_btn = Button(
            image=None, pos=(center_x, 300), font=self.font,
            base_color=(200, 200, 200), hovering_color=(255, 255, 0),
            text_input=theme_text, callback=self.cycle_theme
        )
        self.buttons.append(self.theme_btn)

        sound_text = "Sound: ON" if self.game.context.sound_enabled else "Sound: OFF"
        self.sound_btn = Button(
            image=None, pos=(center_x, 400), font=self.font,
            base_color=(200, 200, 200), hovering_color=(255, 255, 0),
            text_input=sound_text, callback=self.toggle_sound
        )
        self.buttons.append(self.sound_btn)

        self.back_btn = Button(
            image=None, pos=(center_x, 520), font=self.font,
            base_color=(255, 100, 100), hovering_color=(255, 0, 0),
            text_input="Back to Menu", callback=self.go_back
        )
        self.buttons.append(self.back_btn)

    def toggle_mode(self):
        self.game.context.is_speed_increasing = not self.game.context.is_speed_increasing
        new_text = "Mode: Endless Rush" if self.game.context.is_speed_increasing else "Mode: Normal"
        self._update_btn_text(self.mode_btn, new_text)

    def cycle_theme(self):
        current_idx = self.themes.index(self.game.context.background_theme)
        next_idx = (current_idx + 1) % len(self.themes)
        self.game.context.background_theme = self.themes[next_idx]
        
        new_text = f"Theme: {self.game.context.background_theme.capitalize()}"
        self._update_btn_text(self.theme_btn, new_text)

    def toggle_sound(self):
        self.game.context.sound_enabled = not self.game.context.sound_enabled
        new_text = "Sound: ON" if self.game.context.sound_enabled else "Sound: OFF"
        self._update_btn_text(self.sound_btn, new_text)

    def go_back(self):
        self.game.state_machine.change(MENU_SCENE)

    def _update_btn_text(self, btn, text):
        btn.text_input = text
        btn.text = btn.font.render(text, True, btn.base_color)
        btn.rect = btn.text.get_rect(center=(btn.x_pos, btn.y_pos))
        btn.text_rect = btn.text.get_rect(center=(btn.x_pos, btn.y_pos))

    def update(self, dt):
        for btn in self.buttons:
            btn.update(dt)

    def draw(self, screen):
        screen.fill((20, 30, 40))
        
        title = self.title_font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

        for btn in self.buttons:
            btn.draw(screen)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)