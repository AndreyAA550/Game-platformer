import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = pygame.Rect(100, 100, 40, 60)
platform = pygame.Rect(300, 450, 100, 10)
vel_y = 0
gravity = 0.5
speed = 5

ground = pygame.Rect(0, 550, 800, 50)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_SPACE] and player.y == ground.top - player.height:
        vel_y = -12
    if keys[pygame.K_SPACE] and player.y == platform.top - player.height:
        vel_y = -12

    vel_y += gravity
    player.y += vel_y

    if player.colliderect(ground):
        player.y = ground.top - player.height
        vel_y = 0

п
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (200, 200, 200), ground)
    pygame.draw.rect(screen, (100, 180, 255), player)
    pygame.draw.rect(screen, (100, 255, 100), platform)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
