import pygame

class Button:
    def __init__(self, image, pos, font, base_color, hovering_color, text_input, callback=None, bg_color=None, border_radius=0, size=None):
        self.image = image 
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        #scene transition
        self.callback = callback 
        
        self.bg_color = bg_color
        self.border_radius = border_radius

        self.scale = 1.0
        self.target_scale = 1.0
        self.state = "normal"  # normal, hover, click 

        # ===== TEXT =====
        self.text = self.font.render(self.text_input, True, self.base_color)
        if size is not None:
            self.rect = pygame.Rect(self.x_pos, self.y_pos, size[0], size[1])
        elif self.image is None: 
            self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()

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
        
        #color
        if self.bg_color:
            current_bg = self.bg_color
            if self.state == "hover":
                current_bg = (min(self.bg_color[0]+20, 255), min(self.bg_color[1]+20, 255), min(self.bg_color[2]+20, 255))
            elif self.state == "pressed":
                current_bg = (max(self.bg_color[0]-20, 0), max(self.bg_color[1]-20, 0), max(self.bg_color[2]-20, 0))
                
            pygame.draw.rect(screen, current_bg, scaled_rect, border_radius=self.border_radius)
        
        # image 
        if self.image is not None:
            scaled_img = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
            screen.blit(scaled_img, scaled_img.get_rect(center=scaled_rect.center))
            
        # Text
        current_text_color = self.hovering_color if self.state == "hover" else self.base_color
        text_surface = self.font.render(self.text_input, True, current_text_color)
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
