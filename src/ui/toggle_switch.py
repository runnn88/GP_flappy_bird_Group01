import pygame

class ToggleSwitch:
    def __init__(self, x, y, width, height, initial_state=False, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_on = initial_state
        self.callback = callback
        
        self.color_on = (132, 213, 242) # #84D5F2
        self.color_off = (209, 222, 227) # #D1DEE3 
        self.color_knob = (255, 255, 255)
        
        self.is_hovering = False

    def update(self, dt):
        pass

    def draw(self, screen):
        radius = self.rect.height // 2
        bg_color = self.color_on if self.is_on else self.color_off

        pygame.draw.rect(screen, bg_color, self.rect, border_radius=radius)
        knob_size = self.rect.height
        
        if self.is_on:
            knob_x = self.rect.right - knob_size
        else:
            knob_x = self.rect.left 
            
        knob_y = self.rect.top 
        
        knob_rect = pygame.Rect(int(knob_x), int(knob_y), int(knob_size), int(knob_size))
        pygame.draw.rect(screen, self.color_knob, knob_rect, border_radius=int(knob_size//2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_on = not self.is_on
                if self.callback:
                    self.callback(self.is_on)