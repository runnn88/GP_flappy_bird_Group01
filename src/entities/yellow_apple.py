from src.entities.coin import APPLE_COLORS, Coin


YELLOW_APPLE_COLORS = {
    1: (255, 214, 10),
    2: (188, 146, 0),
    3: APPLE_COLORS[3],
    4: (255, 250, 210),
}


class YellowApple(Coin):
    GLOW_COLOR = (255, 235, 100, 110)
    PIXEL_COLORS = YELLOW_APPLE_COLORS
    _cached_frames = None

    def is_flip_apple(self):
        return True
