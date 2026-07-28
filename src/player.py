from pygame import Rect, transform


class Player:
    def __init__(self, frames, start_x, start_y, animation_speed):
        self.frames = frames
        self.x_force_active = False
        self.on_ground = False
        self.on_ground_platform = None
        self.animation_timer = 0
        self.animation_speed = animation_speed
        self.player_current_frame = 0

        self.rect = Rect(start_x, start_y, self.frames[0].get_width(), self.frames[0].get_height())
        self.max_speed = 5
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_go_right = True

    def __str__(self):
        return '\n'.join(f'{k} = {repr(v)}' for k, v in self.__dict__.items())

    def apply_gravity(self, gravity):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.next_frame()
        self.velocity_y += gravity

    def left(self):
        self.x_force_active = True
        self.velocity_x = max(self.velocity_x - 1, - self.max_speed)
        self.is_go_right = False

    def right(self):
        self.x_force_active = True
        self.velocity_x = min(self.velocity_x + 1, self.max_speed)
        self.is_go_right = True

    def stop(self):
        self.x_force_active = False

    def respawn(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 0
        self.velocity_y = 0

    def vertical_hit(self, platform):
        if self.rect.y <= platform.rect.y and self.velocity_y >= platform.velocity_y:
            self.land_on(platform)
        if self.rect.y >= platform.rect.y and self.velocity_y <= platform.velocity_y:
            self.hit_ceiling(platform)

    def land_on(self, platform):
        self.rect.bottom = platform.rect.top
        self.velocity_y = platform.velocity_y
        self.on_ground = True
        self.on_ground_platform = platform
        platform.player_stand()

    def hit_ceiling(self, platform):
        self.rect.top = platform.rect.bottom
        self.velocity_y = platform.velocity_y

    def horizontal_hit(self, rect):
        if self.velocity_x > 0:
            self.rect.right = rect.left
        else:
            self.rect.left = rect.right

    def jump(self):
        if self.on_ground:
            self.on_ground = False
            self.velocity_y = -12
            self.on_ground_platform = None
            return True
        else:
            return False

    def fly(self):
        if not self.on_ground_platform or not (
            self.on_ground_platform.rect.top == self.rect.bottom and
            self.rect.left <= self.on_ground_platform.rect.right and
            self.rect.right >= self.on_ground_platform.rect.left
        ):
            self.on_ground = False
            self.on_ground_platform = None

    def vertical_update(self):
        self.rect.y += self.velocity_y

    def horizontal_update(self):
        if not self.x_force_active and self.velocity_x:
            self.go_by_inertia()
        self.rect.x += self.velocity_x

    def go_by_inertia(self):
        if self.velocity_x > 0:
            self.velocity_x -= 1
        elif self.velocity_x < 0:
            self.velocity_x += 1

    def get_frame(self):
        if self.is_go_right:
            return self.frames[self.player_current_frame]
        else:
            return transform.flip(self.frames[self.player_current_frame], True, False)

    def next_frame(self):
        if self.velocity_x and self.on_ground:
            self.player_current_frame = (self.player_current_frame + 1) % len(self.frames)
        else:
            self.player_current_frame = 0

    def draw(self, screen, camera_x):
        screen.blit(self.get_frame(), (self.rect.x - camera_x, self.rect.y))

