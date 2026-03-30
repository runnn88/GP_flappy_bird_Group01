import pygame
import os

def load_image(path, size=None):
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img

def load_font(font_name, size):
    path = os.path.join("assets", "fonts", font_name)
    try: 
        return pygame.font.Font(path, size)
    except FileNotFoundError:
        print(f"Cannot find file font {font_name} at path {path}.")
        return pygame.font.SysFont(None, size)        