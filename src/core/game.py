import pygame
from config import WIDTH, HEIGHT, FPS
from src.core.state_machine import StateMachine
from src.scenes.game_scene import GameScene

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.state_machine = StateMachine()
        self.state_machine.change(GameScene(self))

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.state_machine.handle_event(event)

            self.state_machine.update(dt)
            self.state_machine.draw(self.screen)

            pygame.display.flip()

        pygame.quit()   