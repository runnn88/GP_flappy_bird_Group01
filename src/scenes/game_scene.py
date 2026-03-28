import pygame
from src.core.scene_names import GAME_OVER_SCENE
from src.scenes.base_scene import BaseScene
from src.entities.player import Player
from src.systems.parallax_system import ParallaxSystem
from src.systems.spawn_system import SpawnSystem

class GameScene(BaseScene):
    def enter(self):
        self.player = Player()
        self.parallax = ParallaxSystem()
        self.spawner = SpawnSystem()

        self.pipes = []
        self.coins = []
        self.score = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()

        self.player.update(dt, keys)
        self.parallax.update(dt)

        self.spawner.update(dt, self.pipes, self.coins)

        for p in self.pipes:
            p.update(dt)
        self.pipes = [p for p in self.pipes if not p.offscreen()]

        for c in self.coins:
            c.update(dt)
        self.coins = [c for c in self.coins if not c.offscreen()]

        for p in self.pipes:
            if p.collides(self.player.rect()):
                self.trigger_game_over()
                return

        for c in self.coins[:]:
            if self.player.rect().colliderect(c.rect()):
                self.coins.remove(c)
                self.score += 1

        if self.player.y < 0 or self.player.y > 600:
            self.trigger_game_over()

    def draw(self, screen):
        self.parallax.draw(screen)

        for p in self.pipes:
            p.draw(screen)

        for c in self.coins:
            c.draw(screen)

        self.player.draw(screen)

    def handle_event(self, event):
        pass

    def trigger_game_over(self):
        self.game.state_machine.change(GAME_OVER_SCENE, score=self.score)
