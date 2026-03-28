class BaseScene:
    def __init__(self, game):
        self.game = game

    def enter(self): pass
    def exit(self): pass
    def update(self, dt): pass
    def draw(self, screen): pass
    def handle_event(self, event): pass