import pygame
from src.core.scene_names import GAME_SCENE, MENU_SCENE
from src.scenes.base_scene import BaseScene
from src.systems.parallax_system import ParallaxSystem
from src.ui.background_renderer import BackgroundRenderer
from src.utils.loader import load_font

# dùng lại apple sprite
from src.entities.coin import create_pixel_sprite, APPLE_MATRIX, APPLE_COLORS


class GameOverScene(BaseScene):
    def enter(self):
        self.title_font = load_font("VT323-Regular.ttf", 80)
        self.text_font = load_font("VT323-Regular.ttf", 40)
        # self.parallax = ParallaxSystem(self.game.context.background_theme)
        # self.background_renderer = BackgroundRenderer()
        # self.slider_dragging = False
        
        # self.themes = ["noon", "sunset", "night", "sunrise"]

        # tạo icon apple
        self.apple_icon = create_pixel_sprite(APPLE_MATRIX, 5, APPLE_COLORS)

    def update(self, dt):
        pass

    def draw(self, screen):
        w, h = screen.get_size()

        # ===== BACKGROUND =====
        screen.fill((10, 10, 20))  # xanh đen nhẹ thay vì đen cứng
        # self.background_renderer.draw(screen, self.parallax)

        # ===== PANEL BACKGROUND (semi-transparent) =====
        # panel_width = 400
        # panel_height = 300

        # panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        # panel.fill((20, 20, 30, 100))  # alpha ~40%
        # pygame.draw.rect(
        #     panel,
        #     (255, 255, 255, 60),  # viền trắng mờ
        #     panel.get_rect(),
        #     2,  # độ dày viền
        #     border_radius=10  # bo góc nhẹ
        # )

        # panel_rect = panel.get_rect(center=(w // 2, h // 2))
        # screen.blit(panel, panel_rect)


        # ===== TITLE (có glow nhẹ) =====
        title_text = self.title_font.render("GAME OVER", True, (255, 60, 60))

        glow = self.title_font.render("GAME OVER", True, (255, 0, 0))
        glow.set_alpha(80)

        title_rect = title_text.get_rect(center=(w // 2, h // 4))

        # vẽ glow trước
        for offset in [(-2,0),(2,0),(0,-2),(0,2)]:
            screen.blit(glow, title_rect.move(offset))

        screen.blit(title_text, title_rect)

        # ===== SCORE =====
        score_text = self.text_font.render(
            f"Score: {self.game.context.score}", True, (255, 255, 255)
        )
        score_rect = score_text.get_rect(center=(w // 2, h // 2 - 20))
        screen.blit(score_text, score_rect)

        # ===== APPLE ICON =====
        icon_rect = self.apple_icon.get_rect(center=(w // 2, score_rect.top - 50))
        screen.blit(self.apple_icon, icon_rect)

        # ===== INSTRUCTIONS =====
        retry_text = self.text_font.render("Press R to Retry", True, (180, 255, 180))
        menu_text = self.text_font.render("Press ESC for Menu", True, (180, 180, 255))

        retry_rect = retry_text.get_rect(center=(w // 2, h // 2 + 60))
        menu_rect = menu_text.get_rect(center=(w // 2, h // 2 + 110))

        screen.blit(retry_text, retry_rect)
        screen.blit(menu_text, menu_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.game.state_machine.change(GAME_SCENE)

            if event.key == pygame.K_ESCAPE:
                self.game.state_machine.change(MENU_SCENE)