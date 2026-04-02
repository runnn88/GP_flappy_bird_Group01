import random

import pygame
from config import (
    FLIPPED_DURATION_MAX_POINTS,
    FLIPPED_DURATION_MIN_POINTS,
    FLIPPED_START_SCORE,
    FLIPPED_TRIGGER_MAX_GAP,
    FLIPPED_TRIGGER_MIN_GAP,
    GRAVITY,
    HEIGHT,
    MAX_SCROLL_SPEED,
    SCROLL_SPEED,
    SPEED_INCREASE_INTERVAL,
    SPEED_INCREASE_STEP,
    THEME_ROTATION_INTERVAL,
)
from src.core.scene_names import GAME_OVER_SCENE, PAUSE_SCENE
from src.scenes.base_scene import BaseScene
from src.entities.player import Player
from src.systems.parallax_system import ParallaxSystem
from src.systems.spawn_system import SpawnSystem
from src.ui.renderer import SceneRenderer

class GameScene(BaseScene):
    def enter(self):
        self.game.audio.play_music("game", restart=True)
        self.player = Player()
        self.parallax = ParallaxSystem(self.game.context.background_theme)
        self.spawner = SpawnSystem()
        self.renderer = SceneRenderer()

        self.pipes = []
        self.coins = []
        self.elapsed_time = 0
        self.speed_interval_timer = 0
        self.game.context.score = 0
        self.game.context.is_game_over = False
        self.game.context.gravity = GRAVITY
        self.game.context.scroll_speed = SCROLL_SPEED
        self.game.context.background_theme = "noon"
        self.game.context.is_flipped = False
        self.game.context.pending_flip_apple = False
        self.game.context.next_flip_spawn_score = FLIPPED_START_SCORE
        self.game.context.flip_exit_spawn_score = None
        self.game.context.pre_flip_theme = "noon"
        self._configure_theme_cycle("noon")

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.elapsed_time += dt
        self.speed_interval_timer += dt

        self._update_scroll_speed()
        self._update_background_theme()

        self.player.update(dt, keys, self.game.context)
        self.parallax.update(dt, self.game.context)

        for p in self.pipes:
            p.update(dt, self.game.context)
        self.pipes = [p for p in self.pipes if not p.offscreen()]

        for c in self.coins:
            c.update(dt, self.game.context)
        self.coins = [c for c in self.coins if not c.offscreen()]

        self._update_flip_objectives()
        self.spawner.update(dt, self.pipes, self.coins, self.game.context)

        for p in self.pipes:
            if p.collides(self.player.rect()):
                self.trigger_game_over()
                return

        for c in self.coins[:]:
            if self.player.rect().colliderect(c.rect()):
                self.coins.remove(c)
                self.game.context.score += 1
                self.game.audio.play_sfx("point")
                if c.is_flip_apple():
                    if self.game.context.is_flipped:
                        self._deactivate_flipped_mode()
                    else:
                        self._activate_flipped_mode()

        if self.player.y < 0 or self.player.y + 50 > HEIGHT:
            self.trigger_game_over()

    def draw(self, screen):
        self.renderer.draw_game(screen, self)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state_machine.change(PAUSE_SCENE, previous_scene=self)

    def _update_scroll_speed(self):
        if self.game.context.game_mode != "rising":
            self.game.context.scroll_speed = SCROLL_SPEED
            self.speed_interval_timer = 0
            return

        while (
            self.speed_interval_timer >= SPEED_INCREASE_INTERVAL
            and self.game.context.scroll_speed < MAX_SCROLL_SPEED
        ):
            self.speed_interval_timer -= SPEED_INCREASE_INTERVAL
            self.game.context.scroll_speed = min(
                MAX_SCROLL_SPEED,
                self.game.context.scroll_speed + SPEED_INCREASE_STEP,
            )

    def _update_background_theme(self):
        if self.game.context.is_flipped:
            self.game.context.background_theme = "flipped"
            return

        theme_index = int(self.elapsed_time / THEME_ROTATION_INTERVAL) % len(self.theme_cycle)
        self.game.context.background_theme = self.theme_cycle[theme_index]

    def _configure_theme_cycle(self, selected_theme):
        base_theme_cycle = ["noon", "sunset", "night", "sunrise"]
        if selected_theme in base_theme_cycle:
            start_index = base_theme_cycle.index(selected_theme)
            self.theme_cycle = base_theme_cycle[start_index:] + base_theme_cycle[:start_index]
        else:
            self.theme_cycle = base_theme_cycle

    def _update_flip_objectives(self):
        has_flip_apple = any(coin.is_flip_apple() for coin in self.coins)
        if self.game.context.pending_flip_apple or has_flip_apple:
            return

        if self.game.context.is_flipped:
            target_score = self.game.context.flip_exit_spawn_score
        else:
            target_score = self.game.context.next_flip_spawn_score

        if target_score is not None and self.game.context.score >= target_score:
            self.game.context.pending_flip_apple = True

    def _activate_flipped_mode(self):
        self.game.context.pre_flip_theme = self.game.context.background_theme
        self.game.context.is_flipped = True
        self.game.context.gravity = -GRAVITY
        self.game.context.background_theme = "flipped"
        self.game.context.pending_flip_apple = False
        self.game.context.flip_exit_spawn_score = self.game.context.score + random.randint(
            FLIPPED_DURATION_MIN_POINTS,
            FLIPPED_DURATION_MAX_POINTS,
        )
        self.parallax.set_theme("flipped")

    def _deactivate_flipped_mode(self):
        restored_theme = self.game.context.pre_flip_theme or "noon"
        self.game.context.is_flipped = False
        self.game.context.gravity = GRAVITY
        self.game.context.background_theme = restored_theme
        self.game.context.pending_flip_apple = False
        self.game.context.flip_exit_spawn_score = None
        self.game.context.next_flip_spawn_score = self.game.context.score + random.randint(
            FLIPPED_TRIGGER_MIN_GAP,
            FLIPPED_TRIGGER_MAX_GAP,
        )
        self.elapsed_time = 0
        self._configure_theme_cycle(restored_theme)
        self.parallax.set_theme(restored_theme)

    def trigger_game_over(self):
        self.game.context.is_game_over = True
        self.game.audio.play_sfx("boom")
        self.game.state_machine.change(GAME_OVER_SCENE)
