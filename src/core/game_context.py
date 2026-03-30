class GameContext:
    def __init__(self):
        self.score = 0
        self.is_game_over = False
        self.scroll_speed = 200
        self.gravity = 1200
        self.background_theme = "noon"
        self.is_speed_increasing = False
        self.sound_enabled = True