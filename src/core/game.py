import pygame
from config import WIDTH, HEIGHT, FPS
from src.core.audio_manager import AudioManager
from src.core.game_context import GameContext
from src.core.scene_names import GAME_OVER_SCENE, GAME_SCENE, MENU_SCENE, SETTING_SCENE, PAUSE_SCENE
from src.core.state_machine import StateMachine
from src.core.scene_registry import register

# Import scenes once here to avoid circular imports in scene modules.
from src.scenes.menu_scene import MenuScene
from src.scenes.game_scene import GameScene
from src.scenes.game_over_scene import GameOverScene
from src.scenes.setting_scene import SettingScene
from src.scenes.pause_scene import PauseScene


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.context = GameContext()
        self.audio = AudioManager(self.context)

        register(MENU_SCENE, MenuScene)
        register(GAME_SCENE, GameScene)
        register(GAME_OVER_SCENE, GameOverScene)
        register(SETTING_SCENE, SettingScene)
        register(PAUSE_SCENE, PauseScene)

        self.state_machine = StateMachine(self)
        self.state_machine.change(MENU_SCENE)

    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, 1 / 30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.state_machine.handle_event(event)

            self.state_machine.update(dt)
            self.state_machine.draw(self.screen)

            pygame.display.flip()

        pygame.quit()   
