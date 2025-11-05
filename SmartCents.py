# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.display.set_caption('SmartCents')
pygame.init()
# Screen Size
screen = pygame.display.set_mode((1280, 720))
bg_image = pygame.image.load('Assets/Background/MainBackgroundSmartCents.png')
bg_image = pygame.transform.scale(bg_image, (1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
x = 0
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg_image, (x, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()