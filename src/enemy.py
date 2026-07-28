from pygame import Rect


class FlyingEnemy:
    def __init__(self, frames, start_x, start_y, animation_speed, track):
        self.frames = frames
        self.animation_timer = 0
        self.animation_speed = animation_speed
        self.track = track
        self.player_current_frame = 0
        self.enemy_target_index = 0
        self.rect = Rect(start_x, start_y, self.frames[0].get_width(), self.frames[0].get_height())
        self.speed = 5

    def __str__(self):
        return '\n'.join(f'{k} = {repr(v)}' for k, v in self.__dict__.items())

    def fly(self):
        target_x, target_y = self.track[self.enemy_target_index]
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist != 0:
            self.rect.x += dx / dist * self.speed
            self.rect.y += dy / dist * self.speed

        if dist < self.speed:
            self.enemy_target_index = (self.enemy_target_index + 1) % len(self.track)

    def get_frame(self):
        # TODO pygame.transform.flip
        return self.frames[self.player_current_frame]

    def next_frame(self):
        self.player_current_frame = (self.player_current_frame + 1) % len(self.frames)

    def draw(self, screen, camera_x):
        screen.blit(self.get_frame(), (self.rect.x - camera_x, self.rect.y))
