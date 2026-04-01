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

        self.text = self.font.render(self.text_input, True, self.base_color)
        if size is not None:
            self.rect = pygame.Rect(self.x_pos, self.y_pos, size[0], size[1])
        elif self.image is None: 
            self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, dt):
        pass

    def draw(self, screen):
        if self.bg_color:
            pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.border_radius)
            
        if self.image is not None:
            screen.blit(self.image, self.rect)
            
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)        
        screen.blit(self.text, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()