import pygame
from src.core.scene_names import MENU_SCENE
from src.scenes.base_scene import BaseScene
from src.systems.parallax_system import ParallaxSystem
from src.ui.button import Button
from src.ui.background_renderer import BackgroundRenderer
from src.utils.loader import load_font
from config import WIDTH 

class SettingScene(BaseScene):
    def enter(self):
        self.game.audio.play_music("menu")
        self.font = load_font("VT323-Regular.ttf", 48)
        self.title_font = load_font("PressStart2P-Regular.ttf", 50)
        self.parallax = ParallaxSystem(self.game.context.background_theme)
        self.background_renderer = BackgroundRenderer()
        self.slider_dragging = False
        
        self.themes = ["noon", "sunset", "night", "sunrise"]
        self.buttons = []
        center_x = WIDTH // 2

        mode_text = self._mode_text()
        self.mode_btn = Button(
            image=None, pos=(center_x, 170), font=self.font,
            base_color=(200, 200, 200), hovering_color=(255, 255, 0),
            text_input=mode_text, callback=self.toggle_mode
        )
        self.buttons.append(self.mode_btn)

        theme_text = f"Theme: {self.game.context.background_theme.capitalize()}"
        self.theme_btn = Button(
            image=None, pos=(center_x, 260), font=self.font,
            base_color=(200, 200, 200), hovering_color=(255, 255, 0),
            text_input=theme_text, callback=self.cycle_theme
        )
        self.buttons.append(self.theme_btn)

        pipe_motion_text = self._pipe_motion_text()
        self.pipe_motion_btn = Button(
            image=None, pos=(center_x, 350), font=self.font,
            base_color=(200, 200, 200), hovering_color=(255, 255, 0),
            text_input=pipe_motion_text, callback=self.toggle_pipe_motion
        )
        self.buttons.append(self.pipe_motion_btn)

        self.volume_label = self.font.render("Music Volume", True, (220, 220, 220))
        self.volume_label_rect = self.volume_label.get_rect(center=(center_x, 450))
        self.slider_rect = pygame.Rect(center_x - 95, 480, 190, 10)
        self.slider_hit_rect = pygame.Rect(center_x - 120, 464, 240, 42)
        self.speaker_hit_rect = pygame.Rect(self.slider_rect.left - 80, self.slider_rect.centery - 24, 52, 48)

        self.back_btn = Button(
            image=None, pos=(center_x, 555), font=self.font,
            base_color=(255, 100, 100), hovering_color=(255, 0, 0),
            text_input="Back to Menu", callback=self.go_back
        )
        self.buttons.append(self.back_btn)

    def toggle_mode(self):
        self.game.context.game_mode = "steady" if self.game.context.game_mode == "rising" else "rising"
        self._update_btn_text(self.mode_btn, self._mode_text())

    def cycle_theme(self):
        current_idx = self.themes.index(self.game.context.background_theme)
        next_idx = (current_idx + 1) % len(self.themes)
        self.game.context.background_theme = self.themes[next_idx]
        self.parallax.set_theme(self.game.context.background_theme)
        
        new_text = f"Theme: {self.game.context.background_theme.capitalize()}"
        self._update_btn_text(self.theme_btn, new_text)

    def toggle_pipe_motion(self):
        self.game.context.pipes_move_vertically = not self.game.context.pipes_move_vertically
        self._update_btn_text(self.pipe_motion_btn, self._pipe_motion_text())

    def toggle_sound(self):
        enabled = not self.game.context.sound_enabled
        self.game.audio.set_sound_enabled(enabled)

    def go_back(self):
        self.game.state_machine.change(MENU_SCENE)

    def _mode_text(self):
        return "Mode: Rising Speed" if self.game.context.game_mode == "rising" else "Mode: Normal Speed"

    def _pipe_motion_text(self):
        return "Moving Pipes: ON" if self.game.context.pipes_move_vertically else "Moving Pipes: OFF"

    def _update_btn_text(self, btn, text):
        btn.set_text(text)

    def _slider_knob_center_x(self):
        return self.slider_rect.left + (self.slider_rect.width * self.game.context.music_volume)

    def _set_volume_from_mouse(self, mouse_x):
        volume = (mouse_x - self.slider_rect.left) / self.slider_rect.width
        self.game.audio.set_music_volume(volume)

    def _draw_volume_control(self, screen):
        speaker_color = (255, 232, 143) if self.game.context.sound_enabled else (145, 145, 145)
        muted_color = (240, 110, 110)
        icon_x = self.slider_rect.left - 55
        icon_y = self.slider_rect.centery

        body_points = [
            (icon_x - 10, icon_y - 10),
            (icon_x - 2, icon_y - 10),
            (icon_x + 8, icon_y - 18),
            (icon_x + 8, icon_y + 18),
            (icon_x - 2, icon_y + 10),
            (icon_x - 10, icon_y + 10),
        ]
        pygame.draw.polygon(screen, speaker_color, body_points)

        if self.game.context.sound_enabled:
            for radius in (14, 22):
                arc_rect = pygame.Rect(icon_x - 2, icon_y - radius, radius * 2, radius * 2)
                pygame.draw.arc(screen, speaker_color, arc_rect, -0.8, 0.8, 3)
        else:
            pygame.draw.line(screen, muted_color, (icon_x + 10, icon_y - 12), (icon_x + 26, icon_y + 12), 4)
            pygame.draw.line(screen, muted_color, (icon_x + 26, icon_y - 12), (icon_x + 10, icon_y + 12), 4)

        pygame.draw.rect(screen, (68, 72, 86), self.slider_rect, border_radius=5)
        fill_width = max(0, int(self.slider_rect.width * self.game.context.music_volume))
        if fill_width > 0:
            fill_rect = pygame.Rect(self.slider_rect.left, self.slider_rect.top, fill_width, self.slider_rect.height)
            pygame.draw.rect(screen, (255, 211, 97), fill_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 247, 214), self.slider_rect, 2, border_radius=5)

        knob_center = (int(self._slider_knob_center_x()), self.slider_rect.centery)
        pygame.draw.circle(screen, (255, 252, 239), knob_center, 11)
        pygame.draw.circle(screen, (160, 120, 35), knob_center, 11, 2)

        percent_text = self.font.render(f"{int(self.game.context.music_volume * 100)}%", True, (250, 250, 250))
        percent_rect = percent_text.get_rect(midleft=(self.slider_rect.right + 16, self.slider_rect.centery))
        screen.blit(self.volume_label, self.volume_label_rect)
        screen.blit(percent_text, percent_rect)

    def update(self, dt):
        self.parallax.update(dt, self.game.context)
        for btn in self.buttons:
            btn.update(dt)

    def draw(self, screen):
        self.background_renderer.draw(screen, self.parallax)
        
        title = self.title_font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

        for btn in self.buttons:
            btn.draw(screen)
        self._draw_volume_control(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.speaker_hit_rect.collidepoint(event.pos):
                self.toggle_sound()
                return
            if self.slider_hit_rect.collidepoint(event.pos):
                self.slider_dragging = True
                self._set_volume_from_mouse(event.pos[0])

        if event.type == pygame.MOUSEMOTION and self.slider_dragging:
            self._set_volume_from_mouse(event.pos[0])

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.slider_dragging = False

        for btn in self.buttons:
            btn.handle_event(event)
