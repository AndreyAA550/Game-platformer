import pygame
from level import levels
from src.enemy import FlyingEnemy
from src.player import Player

WIDTH, HEIGHT = 800, 600
CAMERA_MARGIN = WIDTH * 0.4  # зона покоя

class Game:
    def __init__(self, app):

        self.time_left = 0
        self.camera_x = 0
        self.jump_held = False
        self.lives = 0
        self.jump_sound = pygame.mixer.Sound("../jump.wav")
        self.hit_sound = pygame.mixer.Sound("../hit.wav")
        self.win_sound = pygame.mixer.Sound("../win.wav")

        self.app = app
        self.screen = app.screen
        self.background = pygame.image.load("../background.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        player_image = pygame.transform.scale_by(pygame.image.load("../person.png").convert_alpha(), 1.5)
        player_frames = [player_image.subsurface(pygame.Rect(i * 27 * 1.5, 0, 27 * 1.5, 48 * 1.5)) for i in range(3)]

        flying_enemy_image = pygame.transform.scale_by(pygame.image.load("../enemy.png").convert_alpha(), 2)
        flying_enemy_frames = [flying_enemy_image.subsurface(pygame.Rect(i * 20 * 2, 0, 20 * 2, 32 * 2)) for i in range(2)]

        self.player = Player(player_frames, 100, 100, 24)
        self.flying_enemy = FlyingEnemy(flying_enemy_frames, 2000, 100, 36, [(2000, 100), (1000, 300)])

        self.levels = levels
        self.current_level = 0
        self.level = self.levels[self.current_level]
        self.debug = False

        self.prev_touched = set()
        self.current_touched = set()

    def start(self):
        self.lives = 4
        self.restart_level()

    def restart_level(self):
        self.level = self.levels[self.current_level]
        self.player.respawn(self.level.start_x, self.level.start_y)

        self.jump_held = False
        self.camera_x = 0
        self.time_left = self.level.time_left

        for platform in self.level.platforms:
            platform.reset()

    def update(self, dt):
        for platform in self.level.platforms:
            platform.update(dt, self.player)

        # TODO low gravity while falling if space keydown
        self.player.apply_gravity(self.level.low_gravity if self.jump_held else self.level.gravity)

        self.player.vertical_update()
        self.resolve_player_vertical_collisions()

        self.player.horizontal_update()
        self.resolve_player_horizontal_collisions()

        self.update_touching()

        self.flying_enemy.fly()
        self.resolve_player_enemies_collisions()
        self.resolve_player_finish_collisions()

        self.update_camera()
        self.update_time(dt)

    def update_time(self, delta_time):
        self.time_left -= delta_time
        if self.time_left <= 0:
            self.player_death("TIME OUT")

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (-self.camera_x * 0.3, 0))

        if self.debug:
            lines = str(self.player).split('\n')
            for i, line in enumerate(lines):
                text = pygame.font.SysFont(None, 24).render(line, True, (255, 255, 255))
                self.screen.blit(text, (10, 10 + i * 20))
        else:
            lives_text = pygame.font.SysFont(None, 32).render(f"Lives: {self.lives}", True, (255, 255, 255))
            time_left_text = pygame.font.SysFont(None, 32).render(f"Time Left:{self.time_left:.1f}", True, (255, 255, 255))
            self.screen.blit(lives_text, (10, 10))
            self.screen.blit(time_left_text, (10, 45))

        for world_obj in self.level.obstacles + self.level.ground + self.level.platforms + [self.level.finish_platform, self.player, self.flying_enemy]:
            world_obj.draw(self.screen, self.camera_x)
        pygame.display.flip()

    def show_message(self, text, duration=1000):
        message = pygame.font.SysFont(None, 72).render(text, True, (255, 255, 255))
        rect = message.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        self.screen.fill((0, 0, 0))
        self.screen.blit(message, rect)
        pygame.display.flip()
        pygame.time.delay(duration)  # задержка в миллисекундах

    def resolve_player_horizontal_collisions(self):
        for platform in self.level.ground + self.level.platforms:
            if not platform.is_solid():
                continue

            if self.player.rect.colliderect(platform.rect):
                self.player.horizontal_hit(platform.rect)
                self.current_touched.add(platform)

    def resolve_player_vertical_collisions(self):
        for platform in self.level.ground + self.level.platforms:
            if not platform.is_solid():
                continue

            if self.player.rect.colliderect(platform.rect):
                self.player.vertical_hit(platform)
                self.current_touched.add(platform)
                break

        else:
            self.player.fly()

    def resolve_player_enemies_collisions(self):
        for enemy in self.level.obstacles + [self.flying_enemy]:
            if self.player.rect.colliderect(enemy):
                self.player_death("CRASH")

    def player_death(self, message):
        self.hit_sound.play()
        self.lives -= 1
        if self.lives != 0:
            self.show_message(message)
        else:
            self.show_message("GAME OVER!!!")
            self.app.mode = "menu"
        self.restart_level()

    def player_win(self):
        self.win_sound.play()
        self.show_message("WIN!", 1700)
        self.current_level = (self.current_level + 1) % len(self.levels)
        self.restart_level()

    def resolve_player_finish_collisions(self):
        if self.player.rect.colliderect(self.level.finish_platform.rect):
            self.player_win()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.jump():
                        self.jump_held = True
                        self.jump_sound.play()

                if event.key == pygame.K_d:
                    self.debug = not self.debug

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.jump_held = False

                if event.key == pygame.K_LEFT:
                    self.player.stop()

                if event.key == pygame.K_RIGHT:
                    self.player.stop()

    def handle_keys(self, keys):
        if keys[pygame.K_LEFT]:
            self.player.left()

        if keys[pygame.K_RIGHT]:
            self.player.right()

    def update_camera(self):
        left_border = self.camera_x + CAMERA_MARGIN
        right_border = self.camera_x + WIDTH - CAMERA_MARGIN

        if self.player.rect.x < left_border:
            self.camera_x -= left_border - self.player.rect.x
        elif self.player.rect.x > right_border:
            self.camera_x += self.player.rect.x - right_border

        # ограничение камеры границами уровня
        self.camera_x = max(0, min(self.camera_x, self.level.width - WIDTH))

    def update_touching(self):
        for level_obj in self.prev_touched - self.current_touched:
            level_obj.untouch()
        self.prev_touched = self.current_touched
        self.current_touched = set()


