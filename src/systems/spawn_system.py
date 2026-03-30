from config import MAX_OBSTACLE_SPACING, MAX_SCROLL_SPEED, OBSTACLE_SPACING, SCROLL_SPEED
from src.entities.pipe import Pipe
from src.entities.coin import Coin

class SpawnSystem:
    def __init__(self):
        self.timer = 0

    def update(self, dt, pipes, coins, context):
        self.timer += dt
        spawn_spacing = self._get_spawn_spacing(context)
        spawn_time = spawn_spacing / context.scroll_speed
        if self.timer >= spawn_time:
            self.timer = 0
            pipe = Pipe()
            pipes.append(pipe)
            coins.append(self._spawn_coin(pipe))

    def _get_spawn_spacing(self, context):
        if context.game_mode != "rising":
            return OBSTACLE_SPACING

        speed_range = MAX_SCROLL_SPEED - SCROLL_SPEED
        if speed_range <= 0:
            return OBSTACLE_SPACING

        speed_progress = (context.scroll_speed - SCROLL_SPEED) / speed_range
        speed_progress = max(0, min(1, speed_progress))
        spacing_range = MAX_OBSTACLE_SPACING - OBSTACLE_SPACING
        return OBSTACLE_SPACING + (spacing_range * speed_progress)

    def _spawn_coin(self, pipe):
        orb_x = pipe.x + (pipe.width - Coin.SIZE) / 2
        orb_y = pipe.top + (pipe.gap - Coin.SIZE) / 2
        return Coin(orb_x, orb_y)
