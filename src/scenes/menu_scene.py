import pygame
from src.core.scene_names import GAME_SCENE, SETTING_SCENE
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.systems.parallax_system import ParallaxSystem
from src.ui.background_renderer import BackgroundRenderer
from src.utils.loader import load_font, load_image
from config import WIDTH

from src.entities.coin import create_pixel_sprite, APPLE_MATRIX, APPLE_COLORS

class MenuScene(BaseScene):
    def enter(self):
        self.game.audio.play_music("menu")
        self.font = load_font("PressStart2P-Regular.ttf", 50)
        self.body_font = load_font("VT323-Regular.ttf", 50)

        self.parallax = ParallaxSystem(self.game.context.background_theme)
        self.background_renderer = BackgroundRenderer()
        self.slider_dragging = False
        
        self.themes = ["noon", "sunset", "night", "sunrise"]

        center_x = WIDTH // 2

        self.play_btn = Button(image=None, pos=(center_x, 300), font=self.body_font, 
                               base_color=(180, 255, 180), hovering_color=(0,255,120),
                               text_input="Play Game", callback=self.start_game)
        self.setting_btn = Button(image=None, pos=(center_x, 400), font=self.body_font,
                                base_color=(255, 230, 150), hovering_color=(255, 200, 50),
                                text_input="Settings", callback=self.open_settings)

    def start_game(self):
        self.game.state_machine.change(GAME_SCENE)

    def open_settings(self):
        self.game.state_machine.change(SETTING_SCENE)
        
    def update(self, dt):
        self.parallax.update(dt, self.game.context)
        self.play_btn.update(dt)
        self.setting_btn.update(dt)

    def draw(self, screen):
        w, h = screen.get_size()

        # ===== BACKGROUND =====
        self.background_renderer.draw(screen, self.parallax)

        # ===== DARK OVERLAY (giúp chữ nổi hơn) =====
        # overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        # overlay.fill((0, 0, 0, 80))  # mờ nhẹ
        # screen.blit(overlay, (0, 0))

        # ===== TITLE GLOW =====
        # title_text = " HUNGRY CHIKAWA"

        # title_main = self.font.render(title_text, True, (255, 255, 255))
        # title_glow = self.font.render(title_text, True, (255, 100, 100))

        # title_rect = title_main.get_rect(center=(w // 2, 140))
        # import math
        # offset = int(5 * math.sin(pygame.time.get_ticks() * 0.005))
        # title_rect.centery += offset

        # # glow xung quanh
        # for dx, dy in [(-3,0),(3,0),(0,-3),(0,3)]:
        #     screen.blit(title_glow, title_rect.move(dx, dy))

        # screen.blit(title_main, title_rect)

        # apple = create_pixel_sprite(APPLE_MATRIX, 3, APPLE_COLORS)
        # screen.blit(apple, (title_rect.right + 10, title_rect.centery - 10))
        
        
        # ===== TITLE (UPGRADED) =====
        # import math

        # title_text = "HUNGRY CHIKAWA"

        # # ===== ANIMATION =====
        # time = pygame.time.get_ticks()
        # bounce = int(6 * math.sin(time * 0.004))

        # center_x = w // 2
        # base_y = 140 + bounce

        
        # # ===== TEXT LAYERS =====
        # main_color = (255, 255, 255)
        # outline_color = (0, 0, 0)
        # glow_color = (255, 80, 80)

        # # render text
        # title_main = self.font.render(title_text, True, main_color)
        # title_outline = self.font.render(title_text, True, outline_color)
        # title_glow = self.font.render(title_text, True, glow_color)

        # title_rect = title_main.get_rect(center=(center_x, base_y))
        # # shine_x = (time // 5) % title_rect.width
        # # pygame.draw.rect(screen, (255,255,255,40),
        # #     (title_rect.left + shine_x, title_rect.top, 20, title_rect.height))

        # for i in range(title_main.get_height()):
        #     color = (255, 255 - i//2, 255 - i//2)
        #     line = self.font.render(title_text, True, color)


        # # ===== SOFT GLOW (nhiều lớp) =====
        # for i in range(1, 4):
        #     glow = self.font.render(title_text, True, glow_color)
        #     glow.set_alpha(60 // i)
        #     for dx, dy in [(-i,0),(i,0),(0,-i),(0,i)]:
        #         screen.blit(glow, title_rect.move(dx, dy))

        # # ===== OUTLINE =====
        # for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        #     screen.blit(title_outline, title_rect.move(dx, dy))

        # # ===== MAIN TEXT =====
        # screen.blit(title_main, title_rect)

        # # ===== APPLE ICON (gắn vào title) =====
        # apple = create_pixel_sprite(APPLE_MATRIX, 3, APPLE_COLORS)

        # apple_rect = apple.get_rect()
        # apple_rect.midleft = (title_rect.right + 10, title_rect.centery)

        # # bounce nhẹ theo title
        # apple_rect.y += bounce // 2

        # screen.blit(apple, apple_rect)

        # ===== TITLE 2 LINES (UPGRADED) =====
        import math

        time = pygame.time.get_ticks()
        bounce = int(6 * math.sin(time * 0.004))

        center_x = w // 2
        base_y = 120 + bounce

        # ===== TEXT =====
        top_text = "HUNGRY"
        bottom_text = "CHIKAWA"

        # scale font khác nhau để tạo hierarchy
        top_font = load_font("PressStart2P-Regular.ttf", 40)
        bottom_font = load_font("PressStart2P-Regular.ttf", 60)

        # màu
        main_color = (255, 255, 255)
        bottom_color = (255, 220, 220)
        outline_color = (0, 0, 0)
        glow_color = (255, 80, 80)

        # render
        top_main = top_font.render(top_text, True, main_color)
        top_outline = top_font.render(top_text, True, outline_color)

        bottom_main = bottom_font.render(bottom_text, True, main_color)
        bottom_outline = bottom_font.render(bottom_text, True, outline_color)

        # ===== POSITION =====
        top_rect = top_main.get_rect(center=(center_x, base_y))

        # đè nhẹ lên (overlap)
        bottom_rect = bottom_main.get_rect(center=(center_x, base_y + 45))

        # ===== GLOW =====
        for i in range(1, 4):
            glow = bottom_font.render(bottom_text, True, glow_color)
            glow.set_alpha(60 // i)
            for dx, dy in [(-i,0),(i,0),(0,-i),(0,i)]:
                screen.blit(glow, bottom_rect.move(dx, dy))

        # ===== OUTLINE =====
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            screen.blit(top_outline, top_rect.move(dx, dy))
            screen.blit(bottom_outline, bottom_rect.move(dx, dy))

        # ===== MAIN TEXT =====
        screen.blit(top_main, top_rect)
        screen.blit(bottom_main, bottom_rect)
        shadow_rect = bottom_rect.move(3, 3)
        shadow = bottom_font.render(bottom_text, True, (0,0,0))
        screen.blit(shadow, shadow_rect)

        # ===== APPLE ICON =====
        apple = create_pixel_sprite(APPLE_MATRIX, 5, APPLE_COLORS)
        apple_rect = apple.get_rect()

        # đặt gần chữ CHIKAWA (đúng trọng tâm)
        apple_rect.midleft = (bottom_rect.right + 10, bottom_rect.centery)

        # bounce nhẹ theo title
        apple_rect.y += bounce // 2

        screen.blit(apple, apple_rect)


        # ===== PANEL (giữ UI nổi bật) =====
        # panel = pygame.Surface((400, 220), pygame.SRCALPHA)
        # panel.fill((20, 20, 30, 120))  # ~40-50% opacity

        # pygame.draw.rect(panel, (255, 255, 255, 60), panel.get_rect(), 2, border_radius=12)

        # panel_rect = panel.get_rect(center=(w // 2, 360))
        # screen.blit(panel, panel_rect)

        # ===== BUTTONS =====
        self.play_btn.draw(screen)
        self.setting_btn.draw(screen)

    def handle_event(self, event):
        self.play_btn.handle_event(event)
        self.setting_btn.handle_event(event)
