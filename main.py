import pygame

def show_message(screen, text, duration=1000):
    font = pygame.font.SysFont(None, 72)
    message = font.render(text, True, (255, 255, 255))
    rect = message.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    screen.fill((0, 0, 0))
    screen.blit(message, rect)
    pygame.display.flip()
    pygame.time.delay(duration)  # задержка в миллисекундах

pygame.init()
# pygame.mixer.init()

# pygame.mixer.music.load("background.mp3")
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(0.5)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
lives = 3

LEVEL_WIDTH = 2000
START_X = 100
START_Y = 100

FRAME_WIDTH = 32
FRAME_HEIGHT = 76
FRAMES = 3

player_image = pygame.image.load("person.png").convert_alpha()
# jump_sound = pygame.mixer.Sound("jump.wav")
# hit_sound  = pygame.mixer.Sound("hit.wav")

player_frames = []
for i in range(FRAMES):
    frame = player_image.subsurface(pygame.Rect(i*FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
    player_frames.append(frame)

player = pygame.Rect(START_X, START_Y, FRAME_WIDTH, FRAME_HEIGHT)
platforms = [
    pygame.Rect(600, 450, 120, 10),
    pygame.Rect(800, 450, 120, 10),
]
ground = pygame.Rect(0, 550, LEVEL_WIDTH, 50)
obstacle = pygame.Rect(420, 350, 100, 10)

current_frame = 0
frame_image = player_frames[current_frame]
animation_timer = 0
ANIMATION_SPEED = 10
vel_y = 0
gravity = 0.5
MIN_SPEED, MAX_SPEED = 5, 10
speed = MIN_SPEED
camera_x = 0
CAMERA_MARGIN = WIDTH * 0.4  # зона покоя

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= speed
        frame_image = player_frames[current_frame]
        frame_image = pygame.transform.flip(frame_image, True, False)
        moving = True
    if keys[pygame.K_RIGHT] and player.right < LEVEL_WIDTH:
        player.x += speed
        frame_image = player_frames[current_frame]
        moving = True
    if keys[pygame.K_SPACE] and player.y == ground.top - player.height and player.right > ground.left and player.left < ground.right:
        vel_y = -12
        # jump_sound.play()
    for platform in platforms:
        if keys[pygame.K_SPACE] and player.y == platform.top - player.height and player.right > platform.left and player.left < platform.right:
            vel_y = -12
            # jump_sound.play()
    if keys[pygame.K_LCTRL] and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        speed = min(speed + 1, MAX_SPEED)
    else:
        speed = max(speed - 1, MIN_SPEED)

    vel_y += gravity
    player.y += vel_y

    if player.colliderect(ground):
        player.y = ground.top - player.height
        vel_y = 0

    for platform in platforms:
        if player.colliderect(platform):
            if player.colliderect(platform.left + 5, platform.top, platform.width - 10, 1):
                player.y = platform.top - player.height
                vel_y = 0
            elif player.colliderect(platform.left + 5, platform.bottom, platform.width - 10, 1):
                player.y = platform.bottom
                vel_y = 0
            elif player.colliderect(platform.left, platform.top, 1, platform.height):
                player.x = platform.left - player.width
            elif player.colliderect(platform.right, platform.top, 1, platform.height):
                player.x = platform.right
    if player.colliderect(obstacle):
        lives -= 1
        # hit_sound.play()
        player.x = START_X
        player.y = START_Y
        if lives != 0:
            show_message(screen, "TOUCH!!!")
        else:
            # hit_sound.play()
            show_message(screen, "GAME OVER!!!")
            running = False

    left_border = camera_x + CAMERA_MARGIN
    right_border = camera_x + WIDTH - CAMERA_MARGIN

    if player.x < left_border:
        camera_x -= left_border - player.x
    elif player.x > right_border:
        camera_x += player.x - right_border

    # ограничение камеры границами уровня
    camera_x = max(0, min(camera_x, LEVEL_WIDTH - WIDTH))

    animation_timer += 1
    if animation_timer >= ANIMATION_SPEED:
        animation_timer = 0
        if moving:
            current_frame = (current_frame + 1) % FRAMES
        else:
            current_frame = 0


    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (200, 10, 20), obstacle.move(-camera_x, 0))
    pygame.draw.rect(screen, (200, 200, 200), ground.move(-camera_x, 0))
    for platform in platforms:
        pygame.draw.rect(screen, (100, 255, 100), platform.move(-camera_x, 0))
    screen.blit(frame_image, (player.x - camera_x, player.y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
