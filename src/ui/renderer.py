from src.ui.background_renderer import BackgroundRenderer
from src.ui.coin_renderer import CoinRenderer
from src.ui.hud import HUD
from src.ui.pipe_renderer import PipeRenderer
from src.ui.player_renderer import PlayerRenderer


class SceneRenderer:
    def __init__(self):
        self.background = BackgroundRenderer()
        self.pipes = PipeRenderer()
        self.coins = CoinRenderer()
        self.player = PlayerRenderer()
        self.hud = HUD()

    def draw_game(self, screen, game_scene):
        self.background.draw(screen, game_scene.parallax)
        self.pipes.draw(screen, game_scene.pipes, game_scene.game.context.background_theme)
        self.coins.draw(screen, game_scene.coins, game_scene.game.context)
        for bee in game_scene.bees:
            bee.draw(screen)
        self.player.draw(screen, game_scene.player, game_scene.game.context)
        self.hud.draw(screen, game_scene.game.context)
