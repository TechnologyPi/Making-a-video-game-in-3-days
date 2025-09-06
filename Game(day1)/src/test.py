import pygame

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Player and enemy positions in WORLD coordinates
player_pos = pygame.Vector2(1000, 1000)
enemies = [
    pygame.Vector2(900, 950),
    pygame.Vector2(1200, 1100),
    pygame.Vector2(1500, 1000)
]

# Camera offset
camera = pygame.Vector2(0, 0)

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000  # Delta time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement (WASD)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player_pos.y -= 200 * dt
    if keys[pygame.K_s]: player_pos.y += 200 * dt
    if keys[pygame.K_a]: player_pos.x -= 200 * dt
    if keys[pygame.K_d]: player_pos.x += 200 * dt

    # Update camera so player stays centered
    camera.x = player_pos.x - WIDTH // 2
    camera.y = player_pos.y - HEIGHT // 2

    # Draw background
    screen.fill((30, 30, 30))

    # Draw player (convert world → screen coords)
    player_screen_pos = player_pos - camera
    pygame.draw.rect(screen, (0, 255, 0), (*player_screen_pos, 40, 40))

    # Draw enemies (also convert world → screen coords)
    for enemy in enemies:
        enemy_screen_pos = enemy - camera
        pygame.draw.rect(screen, (255, 0, 0), (*enemy_screen_pos, 40, 40))

    pygame.display.flip()

pygame.quit()
