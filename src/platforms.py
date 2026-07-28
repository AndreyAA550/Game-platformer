from pygame import Rect, draw


class Platform:
    def __init__(self, left, top, width, height):
        self.rect = Rect(left, top, width, height)
        self.velocity_y = 0

    def update(self, dt, player):
        pass

    def untouch(self):
        pass

    def draw(self, screen, camera_x):
        draw.rect(screen, (200, 200, 200), self.rect.move(-camera_x, 0))

    def reset(self):
        pass

    def player_stand(self):
        pass

    def is_solid(self):
        return True


class FinishPlatform(Platform):
    def draw(self, screen, camera_x):
        draw.rect(screen, (159, 10, 100), self.rect.move(-camera_x, 0))


class DisappearingPlatform(Platform):
    def __init__(self, left, top, width, height, delay=2.0, hidden_time=2.0):
        super().__init__(left, top, width, height)

        self.delay = delay
        self.hidden_time = hidden_time

        self.reset()

    def update(self, dt, player):
        if self.state == "IDLE":
            pass

        elif self.state == "TRIGGERED":
            self.timer += dt
            if self.timer >= self.delay:
                self.visible = False
                self.state = "HIDDEN"
                self.timer = 0.0

        elif self.state == "HIDDEN":
            self.timer += dt
            if self.timer >= self.hidden_time:
                self.reset()

    def reset(self):
        self.visible = True
        self.state = "IDLE"
        self.timer = 0.0

    def player_stand(self):
        if self.state == "IDLE":
            self.state = "TRIGGERED"
            self.timer = 0.0

    def untouch(self):
        if self.is_solid():
            self.reset()

    def draw(self, screen, camera_x):
        if self.visible:
            draw.rect(screen,(255, 80, int((self.delay - self.timer) / self.delay * 255)), self.rect.move(-camera_x, 0))

    def is_solid(self):
        return self.visible


class FallingPlatform(Platform):
    def __init__(self, left, top, width, height, delay=2.0, falling_time=2.0):
        super().__init__(left, top, width, height)

        self.delay = delay
        self.falling_time = falling_time
        self.start_rect = self.rect.copy()
        self.state = "IDLE"
        self.timer = 0.0

    def reset(self):
        self.state = "IDLE"
        self.timer = 0.0
        self.rect = self.start_rect.copy()
        self.velocity_y = 0

    def update(self, dt, player):
        if self.state == "IDLE":
            pass

        elif self.state == "TRIGGERED":
            self.timer += dt
            if self.timer >= self.delay:
                self.state = "FALLING"
                self.timer = 0.0

        elif self.state == "FALLING":
            self.timer += dt
            self.velocity_y += 0.55
            self.rect.y += self.velocity_y
            if self.timer >= self.falling_time:
                self.reset()

    def player_stand(self):
        if self.state == "IDLE":
            self.state = "TRIGGERED"
            self.timer = 0.0

    def draw(self, screen, camera_x):
        draw.rect(screen,(255, 80, int((self.delay - self.timer) / self.delay * 255)), self.rect.move(-camera_x, 0))

