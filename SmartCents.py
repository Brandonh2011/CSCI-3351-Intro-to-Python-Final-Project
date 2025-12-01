# Example file showing a circle moving on screen
import pygame
from Button import Button

RED = (255,0,0)
GREEN = (0,255,0)
Gray = (128,128,128)

# pygame setup
pygame.display.set_caption('SmartCents')
pygame.init()
# Screen Size and images
x_screen = 1280
y_screen = 720
screen = pygame.display.set_mode((x_screen, y_screen))
# Background with local path in asset file
bg_image = pygame.image.load('Assets/Background/MainBackgroundSmartCents.png')
bg_image = pygame.transform.scale(bg_image, (x_screen, y_screen))

# Text
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# Title text, can use as an outline
title_text = my_font.render('SmartCents!', False, (0, 0, 0))
title_contain = title_text.get_rect(center=(x_screen/2, y_screen/20))

turn_text = my_font.render('Age: 0', False, (0, 0, 0))
turn_container = turn_text.get_rect(center=(x_screen/1.1, y_screen/20))

money_text = my_font.render('Money: your rich', False, (0, 0, 0))
money_container = money_text.get_rect(center=(x_screen/10, y_screen/20))

footer_text = my_font.render('This is a footer', False, (0, 0, 0))
footer_contain = footer_text.get_rect(center=(x_screen/2, y_screen/1.1))

# Icons
# Add bank Icon here
# Add Upgrade Icon here
# Add Event_Log Icon here
# Addd Settings Icon here

#idk
clock = pygame.time.Clock()
running = True
dt = 0
x = 0

# Load icon
bank_icon = pygame.image.load("Assets/Footer/bank.png")
bank_icon = pygame.transform.scale(bank_icon, (120, 120))
upgrade_icon = pygame.image.load("Assets/Footer/Upgrade Hovered.png")
upgrade_icon = pygame.transform.scale(upgrade_icon, (120, 120))
event_icon = pygame.image.load("Assets/Footer/Event Log.png")
event_icon = pygame.transform.scale(event_icon, (120, 120))
settings_icon = pygame.image.load("Assets/Footer/Settings gear.png")
settings_icon = pygame.transform.scale(settings_icon, (120, 120))

# test button
button_width = x_screen / 4
button_height = y_screen / 6
button_x = 0
button_y = y_screen - button_height
B1 = Button(button_x,button_y,button_width,button_height,"",Gray, GREEN, my_font,None)
B2 = Button(button_width, button_y, button_width, button_height, "", Gray, GREEN, my_font, None)
B3 = Button(button_width*2, button_y, button_width, button_height, "", Gray, GREEN, my_font, None)
B4 = Button(button_width*3, button_y, button_width, button_height, "", Gray, GREEN, my_font, None)



# Put things to be displayed below
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
      
    for event in pygame.event.get():
        # handle test button click (will crash)
        B1.handle_event(event)
        B2.handle_event(event)
        B3.handle_event(event)
        B4.handle_event(event)
        if event.type == pygame.QUIT:
            running = False
    #Background image
    screen.blit(bg_image, (x, 0))
    # Title Text
    screen.blit(title_text, title_contain)
    screen.blit(turn_text, turn_container)
    screen.blit(money_text, money_container)
    screen.blit(footer_text, footer_contain)

    # draw test button
    B1.draw(screen)
    bank_rect = bank_icon.get_rect(center=B1.rect.center)
    screen.blit(bank_icon, bank_rect)

    B2.draw(screen)
    upgrade_rect = upgrade_icon.get_rect(center=B2.rect.center)
    screen.blit(upgrade_icon, upgrade_rect)

    B3.draw(screen)
    event_rect = event_icon.get_rect(center=B3.rect.center)
    screen.blit(event_icon, event_rect)

    B4.draw(screen)
    settings_rect = settings_icon.get_rect(center=B4.rect.center)
    screen.blit(settings_icon, settings_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for frame rate
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
