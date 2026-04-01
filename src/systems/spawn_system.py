import random

from config import MAX_OBSTACLE_SPACING, MAX_SCROLL_SPEED, OBSTACLE_SPACING, PIPE_COIN_CLEARANCE, SCROLL_SPEED
from src.entities.pipe import Pipe
from src.entities.coin import Coin
from src.entities.yellow_apple import YellowApple

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
            previous_pipe = pipes[-1] if pipes else None
            pipes.append(pipe)
            coins.append(self._spawn_coin(pipe, spawn_flip_apple=context.pending_flip_apple))
            context.pending_flip_apple = False
            if previous_pipe is not None:
                bridge_coin = self._spawn_between_pairs_coin(previous_pipe, pipe)
                if bridge_coin is not None:
                    coins.append(bridge_coin)

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

    def _spawn_coin(self, pipe, spawn_flip_apple=False):
        orb_x = pipe.x + (pipe.width - Coin.SIZE) / 2
        orb_y = pipe.top + (pipe.gap - Coin.SIZE) / 2
        coin_cls = YellowApple if spawn_flip_apple else Coin
        return coin_cls(orb_x, orb_y, anchor_pipe=pipe)

    def _spawn_between_pairs_coin(self, left_pipe, right_pipe):
        left_center_x = left_pipe.x + (left_pipe.width / 2)
        right_center_x = right_pipe.x + (right_pipe.width / 2)
        coin_x = ((left_center_x + right_center_x) / 2) - (Coin.SIZE / 2)

        upper_bound = min(left_pipe.top, right_pipe.top) + PIPE_COIN_CLEARANCE
        lower_bound = max(
            left_pipe.top + left_pipe.gap,
            right_pipe.top + right_pipe.gap,
        ) - Coin.SIZE - PIPE_COIN_CLEARANCE

        if lower_bound <= upper_bound:
            coin_y = ((left_pipe.gap_y + right_pipe.gap_y) / 2) - (Coin.SIZE / 2)
        else:
            coin_y = random.uniform(upper_bound, lower_bound)

        return Coin(coin_x, coin_y)
