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

        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None: 
            self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.is_hovering = False 

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovering = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
            
        current_color = self.hovering_color if self.is_hovering else self.base_color
        self.text = self.font.render(self.text_input, True, current_color)
        
        screen.blit(self.text, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Chuột trái
            if self.is_hovering and self.callback:
                self.callback()