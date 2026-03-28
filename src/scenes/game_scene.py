import pygame
from src.scenes.base_scene import BaseScene
from src.entities.player import Player
from src.entities.pipe import Pipe
from src.entities.coin import Coin
from src.systems.parallax_system import ParallaxSystem
from config import SPAWN_TIME

class GameScene(BaseScene):
    def enter(self):
        self.player = Player()
        self.pipes = []
        self.coins = []
        self.parallax = ParallaxSystem()

        self.spawn_timer = 0
        self.score = 0
        self.game_over = False

    def update(self, dt):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)

        self.parallax.update(dt)

        # Spawn
        self.spawn_timer += dt
        if self.spawn_timer > SPAWN_TIME:
            self.spawn_timer = 0
            pipe = Pipe()
            self.pipes.append(pipe)
            self.coins.append(Coin(pipe.x, pipe.gap_y))

        # Update pipes
        for pipe in self.pipes:
            pipe.update(dt)

        self.pipes = [p for p in self.pipes if not p.offscreen()]

        # Update coins
        for coin in self.coins:
            coin.update(dt)

        self.coins = [c for c in self.coins if not c.offscreen()]

        # Collision
        for pipe in self.pipes:
            if pipe.collides(self.player.rect()):
                self.game_over = True

        for coin in self.coins[:]:
            if self.player.rect().colliderect(coin.rect()):
                self.coins.remove(coin)
                self.score += 1

        if self.player.y < 0 or self.player.y > 600:
            self.game_over = True

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.parallax.draw(screen)

        for pipe in self.pipes:
            pipe.draw(screen)

        for coin in self.coins:
            coin.draw(screen)

        self.player.draw(screen)

    def handle_event(self, event):
        pass