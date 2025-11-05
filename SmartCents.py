# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.display.set_caption('SmartCents')
pygame.init()
# Screen Size and images
x_screen = 1280
y_screen = 720
screen = pygame.display.set_mode((x_screen, y_screen))
# Background with local path in asset file
bg_image = pygame.image.load('Assets/Background/MainBackgroundSmartCents.png')
bg_image = pygame.transform.scale(bg_image, (1280, 720))

# Text
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# Title text, can use as a outline
text_surface = my_font.render('SmartCents!', False, (0, 0, 0))

#idk
clock = pygame.time.Clock()
running = True
dt = 0
x = 0

# Put things to be displayed below
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Background image
    screen.blit(bg_image, (x, 0))
    # Title Text
    screen.blit(text_surface, (x_screen/3, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()