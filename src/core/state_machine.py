class StateMachine:
    def __init__(self):
        self.state = None

    def change(self, new_state):
        if self.state:
            self.state.exit()
        self.state = new_state
        self.state.enter()

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)

    def handle_event(self, event):
        self.state.handle_event(event)