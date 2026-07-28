from pygame import Rect, draw


class Hazard:
    def __init__(self, left, top, width, height):
        self.rect = Rect(left, top, width, height)
        self.velocity_y = 0

    def update(self, dt, player):
        pass

    def draw(self, screen, camera_x):
        draw.rect(screen, (200, 10, 20), self.rect.move(-camera_x, 0))

    def reset(self):
        pass

    def player_stand(self):
        pass

    def is_solid(self):
        return True


class Obstacle(Hazard):
    pass

