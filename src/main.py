# Example file showing a circle moving on screen
import os
import pygame

# caminho base para as assets
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSET_DIR = os.path.join(BASE_DIR, 'assets')

#subpastas

IMG_DIR = os.path.join(ASSET_DIR, 'images')
SND_DIR = os.path.join(ASSET_DIR, 'sounds')
FNT_DIR = os.path.join(ASSET_DIR, 'fonts')

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
#background = pygame.image.load(os.path.join(IMG_DIR ,'background.png')).convert()
#background = pygame.transform.scale(background, (1280, 720))

original_image = pygame.image.load(os.path.join(IMG_DIR, 'sapo.png')).convert_alpha()
sapo = pygame.transform.scale(original_image, (50,50))

clock = pygame.time.Clock()
running = True
dt = 0

sapo_rect = sapo.get_rect()
player_pos = pygame.Vector2(
    screen.get_width() / 2 - sapo_rect.width / 2,
    screen.get_height() / 2 - sapo_rect.height / 2
)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    screen.fill('purple')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(sapo, player_pos)

    hitbox = pygame.Rect(player_pos.x, player_pos.y, sapo.get_width(), sapo.get_height())

    target = pygame.Rect(300, 0, 160, 280)
    collision = hitbox.colliderect(target)
    pygame.draw.rect(screen, (255 * collision, 255, 0), target)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()