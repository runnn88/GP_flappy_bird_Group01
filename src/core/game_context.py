class GameContext:
    def __init__(self):
        self.score = 0
        self.is_game_over = False
        self.scroll_speed = 200
        self.gravity = 1200
        self.background_theme = "noon"
        self.is_speed_increasing = False
        self.sound_enabled = True
        self.music_volume = 0.4
        self.game_mode = "rising"
        self.pipes_move_vertically = False
        self.is_flipped = False
        self.pending_flip_apple = False
        self.next_flip_spawn_score = 20
        self.flip_exit_spawn_score = None
        self.pre_flip_theme = "noon"
