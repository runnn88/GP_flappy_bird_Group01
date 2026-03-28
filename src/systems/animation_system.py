class Animation:
    def __init__(self, frames, fps):
        self.frames = frames
        self.fps = fps
        self.timer = 0
        self.index = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= 1 / self.fps:
            self.timer = 0
            self.index = (self.index + 1) % len(self.frames)

    def get_frame(self):
        return self.frames[self.index]