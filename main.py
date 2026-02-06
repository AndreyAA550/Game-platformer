import pygame

def show_message(screen, text, duration=2000):
    font = pygame.font.SysFont(None, 72)
    message = font.render(text, True, (255, 255, 255))
    rect = message.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    screen.fill((0, 0, 0))
    screen.blit(message, rect)
    pygame.display.flip()
    pygame.time.delay(duration)  # задержка в миллисекундах

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
lives = 3

LEVEL_WIDTH = 2000
START_X = 100
START_Y = 100

player = pygame.Rect(START_X, START_Y, 40, 60)
platform = pygame.Rect(600, 450, 120, 10)
ground = pygame.Rect(0, 550, LEVEL_WIDTH, 50)
obstacle = pygame.Rect(420, 350, 100, 10)

vel_y = 0
gravity = 0.5
MIN_SPEED, MAX_SPEED = 5, 10
speed = MIN_SPEED
MIN_PLAYER_HEIGHT, MAX_PLAYER_HEIGHT = 40, 60
camera_x = 0
CAMERA_MARGIN = WIDTH * 0.4  # зона покоя

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= speed
    if keys[pygame.K_RIGHT] and player.right < LEVEL_WIDTH:
        player.x += speed
    if keys[pygame.K_SPACE] and player.y == ground.top - player.height and player.right > ground.left and player.left < ground.right:
        vel_y = -12
    if keys[pygame.K_SPACE] and player.y == platform.top - player.height and player.right > platform.left and player.left < platform.right:
        vel_y = -12
    if keys[pygame.K_LCTRL] and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        speed = min(speed + 1, MAX_SPEED)
    else:
        speed = max(speed - 1, MIN_SPEED)
    if keys[pygame.K_DOWN] and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        player.height = MIN_PLAYER_HEIGHT
    else:
        player.height = MAX_PLAYER_HEIGHT

    vel_y += gravity
    player.y += vel_y

    if player.colliderect(ground):
        player.y = ground.top - player.height
        vel_y = 0

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
        show_message(screen, "TOUCH!!!")
        player.x = START_X
        player.y = START_Y
        lives -= 1
        if lives == 0:
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

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (200, 10, 20), obstacle.move(-camera_x, 0))
    pygame.draw.rect(screen, (200, 200, 200), ground.move(-camera_x, 0))
    pygame.draw.rect(screen, (100, 255, 100), platform.move(-camera_x, 0))
    pygame.draw.rect(screen, (100, 180, 255), player.move(-camera_x, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
