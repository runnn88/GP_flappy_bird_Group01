from config import SPAWN_TIME
from src.entities.pipe import Pipe
from src.entities.coin import Coin

class SpawnSystem:
    def __init__(self):
        self.timer = 0

    def update(self, dt, pipes, coins):
        self.timer += dt
        if self.timer >= SPAWN_TIME:
            self.timer = 0
            pipe = Pipe()
            pipes.append(pipe)
            coins.append(Coin(pipe.x, pipe.gap_y))