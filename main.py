import pygame
from src.core.game import Game

pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=128)
pygame.init()
Game().run()
