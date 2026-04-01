import pygame

class Button:
    def __init__(self, image, pos, font, base_color, hovering_color, text_input, callback=None):
        self.image = image 
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        #scene transition
        self.callback = callback

        self.scale = 1.0
        self.target_scale = 1.0
        self.state = "normal"  # normal, hover, click 

        # ===== TEXT =====
        self.text = self.font.render(self.text_input, True, self.base_color)

        self.padding_x = 60
        self.padding_y = 30

        if self.image is None:
            self.rect = pygame.Rect(
                0, 0,
                self.text.get_width() + self.padding_x,
                self.text.get_height() + self.padding_y
            )
            self.rect.center = (self.x_pos, self.y_pos)
        else:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def set_text(self, text):
        self.text_input = text
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.rect.size = (
                self.text.get_width() + self.padding_x,
                self.text.get_height() + self.padding_y,
            )
            self.rect.center = (self.x_pos, self.y_pos)

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        # self.is_hovering = self.rect.collidepoint(mouse_pos)

        if self.rect.collidepoint(mouse_pos):
            if self.state != "pressed":
                self.state = "hover"
            self.target_scale = 1.08
        else:
            if self.state != "pressed":
                self.state = "normal"
            self.target_scale = 1.0

        # smooth scale
        self.scale += (self.target_scale - self.scale) * min(1, dt * 10)

    def draw(self, screen):
        # ===== SCALE RECT =====
        scaled_rect = self.rect.inflate(
            self.rect.width * (self.scale - 1),
            self.rect.height * (self.scale - 1)
        )

        # ===== COLOR =====
        if self.state == "pressed":
            bg_color = (80, 160, 255)
            border_color = (255, 255, 255)
            text_color = (20, 30, 50)
        elif self.state == "hover":
            bg_color = (30, 60, 100, 160)
            border_color = (120, 200, 255)
            text_color = self.hovering_color
        else:
            bg_color = (20, 30, 50, 140)
            border_color = (100, 150, 200)
            text_color = self.base_color

        # ===== GLOW =====
        if self.state == "hover":
            glow = pygame.Surface(scaled_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(
                glow,
                (100, 180, 255, 60),
                glow.get_rect(),
                border_radius=14
            )
            screen.blit(glow, scaled_rect.topleft)

        # ===== BACKGROUND =====
        bg_surface = pygame.Surface(scaled_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            bg_surface,
            bg_color,
            bg_surface.get_rect(),
            border_radius=14
        )
        screen.blit(bg_surface, scaled_rect.topleft)

        # ===== BORDER =====
        pygame.draw.rect(
            screen,
            border_color,
            scaled_rect,
            2,
            border_radius=14
        )

        # ===== TEXT =====
        text_surface = self.font.render(self.text_input, True, text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)

        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.state == "hover":
                self.state = "pressed"
                if self.callback:
                    self.callback()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.state == "pressed":
                self.state = "hover"
