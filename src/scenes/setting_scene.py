import pygame
from src.core.scene_names import MENU_SCENE
from src.scenes.base_scene import BaseScene
from src.systems.parallax_system import ParallaxSystem
from src.ui.button import Button
from src.ui.toggle_switch import ToggleSwitch
from src.ui.background_renderer import BackgroundRenderer
from src.utils.loader import load_font
from config import WIDTH 

class SettingScene(BaseScene):
    def enter(self):
        self.game.audio.play_music("menu")
        
        self.title_font = load_font("PressStart2P-Regular.ttf", 60)
        self.label_font = load_font("VT323-Regular.ttf", 54)
        self.theme_btn_font = load_font("VT323-Regular.ttf", 36)
        self.percent_font = load_font("VT323-Regular.ttf", 36)
        self.back_btn_font = load_font("VT323-Regular.ttf", 48)
        
        self.parallax = ParallaxSystem(self.game.context.background_theme)
        self.background_renderer = BackgroundRenderer()
        self.slider_dragging = False
        
        self.themes = ["noon", "sunset", "night", "sunrise"]
        self.buttons = []
        self.toggles = []
        
        self.label_color = (186, 136, 218) # #BA88DA
        self.theme_text_color = (255, 246, 213) # #FFF6D5
        self.btn_bg_color = (132, 213, 242) # #84D5F2
        self.volume_base_color = (209, 222, 227) # #D1DEE3
        self.back_bg_color = (249, 133, 183) # #F985B7
    
        toggle_w = 109
        toggle_h = 44
        toggle_x = 587
        
        # mode 
        initial_mode = self.game.context.game_mode == "rising"
        self.mode_toggle = ToggleSwitch(
            x=toggle_x, y=147, width=toggle_w, height=toggle_h,
            initial_state=initial_mode, callback=self.toggle_mode
        )
        self.toggles.append(self.mode_toggle)
        
        # Theme
        theme_text = self.game.context.background_theme.upper()
        self.theme_btn = Button(
            image=None, pos=(566,229), font=self.theme_btn_font,
            base_color=self.theme_text_color, hovering_color=self.theme_text_color,
            text_input=theme_text, callback=self.cycle_theme,
            bg_color=self.btn_bg_color, border_radius=20, size=(130,48)
        )
        self.buttons.append(self.theme_btn)

        # Dynamic Obstacle 
        self.pipe_motion_toggle = ToggleSwitch(
            x=toggle_x, y=319, width=toggle_w, height=toggle_h,
            initial_state=self.game.context.pipes_move_vertically, callback=self.toggle_pipe_motion
        )
        self.toggles.append(self.pipe_motion_toggle)

        # Volume
        self.slider_rect = pygame.Rect(444, 426, 172, 12) 
        self.slider_hit_rect = pygame.Rect(430, 400, 200, 50)
        self.speaker_hit_rect = pygame.Rect(450, 380, 50, 60)

        # Back 
        self.back_btn = Button(
            image=None, pos=(315, 470), font=self.back_btn_font,
            base_color=self.theme_text_color, hovering_color=self.theme_text_color,
            text_input="Back", callback=self.go_back,
            bg_color=self.back_bg_color, border_radius=20, size=(170,66)
        )
        self.buttons.append(self.back_btn)

        self.lbl_mode = self.label_font.render("Difficulty Scaling", True, self.label_color)
        self.lbl_theme = self.label_font.render("Theme", True, self.label_color)
        self.lbl_pipe = self.label_font.render("Dynamic Obstacles", True, self.label_color)
        self.lbl_vol = self.label_font.render("Volume", True, self.label_color)

    def toggle_mode(self, new_state):
        self.game.context.game_mode = "rising" if new_state else "steady"

    def cycle_theme(self):
        current_idx = self.themes.index(self.game.context.background_theme)
        next_idx = (current_idx + 1) % len(self.themes)
        self.game.context.background_theme = self.themes[next_idx]
        self.parallax.set_theme(self.game.context.background_theme)
        
        new_text = self.game.context.background_theme.upper()
        self._update_btn_text(self.theme_btn, new_text)

    def toggle_pipe_motion(self, new_state):
        self.game.context.pipes_move_vertically = new_state

    def toggle_sound(self):
        enabled = not self.game.context.sound_enabled
        self.game.audio.set_sound_enabled(enabled)

    def go_back(self):
        self.game.state_machine.change(MENU_SCENE)

    def _update_btn_text(self, btn, text):
        btn.text_input = text
        btn.text = btn.font.render(text, True, btn.base_color)
        btn.text_rect = btn.text.get_rect(center=(btn.x_pos, btn.y_pos))

    def _slider_knob_center_x(self):
        return self.slider_rect.left + (self.slider_rect.width * self.game.context.music_volume)

    def _set_volume_from_mouse(self, mouse_x):
        volume = (mouse_x - self.slider_rect.left) / self.slider_rect.width
        volume = max(0.0, min(1.0, volume)) 
        self.game.audio.set_music_volume(volume)

    def _draw_volume_control(self, screen):
        slider_base_color = self.volume_base_color # #D1DEE3 
        slider_fill_color = self.btn_bg_color # #84D5F2 
       
        pygame.draw.rect(screen, slider_base_color, self.slider_rect, border_radius=6)
        
        # Fill up slider
        fill_width = max(0, int(self.slider_rect.width * self.game.context.music_volume))
        if fill_width > 0:
            fill_rect = pygame.Rect(self.slider_rect.left, self.slider_rect.top, fill_width, self.slider_rect.height)
            pygame.draw.rect(screen, slider_fill_color, fill_rect, border_radius=6) 

        # Knob
        knob_center = (int(self._slider_knob_center_x()), self.slider_rect.centery)
        pygame.draw.circle(screen, (255, 255, 255), knob_center, 11)

        # Percentage
        percent_str = f"{int(self.game.context.music_volume * 100)}%"
        percent_text = self.percent_font.render(percent_str, True, slider_fill_color)
        screen.blit(percent_text, (652, 414))

    def update(self, dt):
        self.parallax.update(dt, self.game.context)
        for btn in self.buttons:
            btn.update(dt)
        for toggle in self.toggles:
            toggle.update(dt)

    def draw(self, screen):
        self.background_renderer.draw(screen, self.parallax)
        
        overlay = pygame.Surface((699, 527), pygame.SRCALPHA) # rgba(255, 242, 208, 0.71) 
        pygame.draw.rect(overlay, (255, 242, 208, 180), overlay.get_rect(), border_radius=25)
        screen.blit(overlay, (54, 37))
        
        title = self.title_font.render("SETTINGS", True, (182, 61, 169)) # #B63DA9
        screen.blit(title, (168, 64))

        screen.blit(self.lbl_mode, (104, 142))
        screen.blit(self.lbl_theme, (104, 228))
        screen.blit(self.lbl_pipe, (104, 314))
        screen.blit(self.lbl_vol, (104, 400))

        for btn in self.buttons:
            btn.draw(screen)
            
        for toggle in self.toggles:
            toggle.draw(screen)
            
        self._draw_volume_control(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.speaker_hit_rect.collidepoint(event.pos):
                self.toggle_sound()
                return
            if pygame.Rect(500, 380, 220, 60).collidepoint(event.pos): # slider_hit_rect
                self.slider_dragging = True
                vol = (event.pos[0] - self.slider_rect.left) / self.slider_rect.width
                vol = max(0.0, min(1.0, vol))
                self.game.audio.set_music_volume(vol)

        if event.type == pygame.MOUSEMOTION and self.slider_dragging:
            vol = (event.pos[0] - self.slider_rect.left) / self.slider_rect.width
            vol = max(0.0, min(1.0, vol))
            self.game.audio.set_music_volume(vol)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.slider_dragging = False

        for btn in self.buttons:
            btn.handle_event(event)
        
        for toggle in self.toggles:
            toggle.handle_event(event)