from src.core.scene_registry import get_scene


class StateMachine:
    def __init__(self, game):
        self.game = game
        self.state = None

    def change(self, scene_name, **kwargs):
        scene_cls = get_scene(scene_name)
        if self.state:
            self.state.exit()
        self.state = scene_cls(self.game, **kwargs)
        self.state.enter()

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)

    def handle_event(self, event):
        self.state.handle_event(event)
