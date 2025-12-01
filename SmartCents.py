# Example file showing a circle moving on screen
import pygame
from Button import Button

RED = (255,0,0)
GREEN = (0,255,0)
Gray = (128,128,128)

# pygame setup
pygame.display.set_caption('SmartCents')
pygame.init()

x_screen = 1280
y_screen = 720
screen = pygame.display.set_mode((x_screen, y_screen))

# Background
bg_image = pygame.image.load('Assets/Background/MainBackgroundSmartCents.png')
bg_image = pygame.transform.scale(bg_image, (x_screen, y_screen))
billy_image = pygame.image.load('Assets/Background/Billy.png')
billy_image = pygame.transform.scale(billy_image, (200, 200))

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

title_text = my_font.render('SmartCents!', False, (0, 0, 0))
title_contain = title_text.get_rect(center=(x_screen/2, y_screen/20))

turn_text = my_font.render('Age: 0', False, (0, 0, 0))
turn_container = turn_text.get_rect(center=(x_screen/1.1, y_screen/20))

money_text = my_font.render('Money: your rich', False, (0, 0, 0))
money_container = money_text.get_rect(center=(x_screen/10, y_screen/20))

footer_text = my_font.render('This is a footer', False, (0, 0, 0))
footer_contain = footer_text.get_rect(center=(x_screen/2, y_screen/1.1))

# POPUP SYSTEM
popups = {
    "bank": False,
    "upgrade": False,
    "event_log": False,
    "settings": False
}

def open_popup(name):
    for key in popups:
        popups[key] = False
    popups[name] = True

def open_Bank(): open_popup("bank")
def open_Upgrade(): open_popup("upgrade")
def open_Event_Log(): open_popup("event_log")
def open_Setting(): open_popup("settings")

clock = pygame.time.Clock()
running = True
dt = 0
x = 0

# Icons
bank_icon = pygame.transform.scale(pygame.image.load("Assets/Footer/Bank.png"), (120, 120))
upgrade_icon = pygame.transform.scale(pygame.image.load("Assets/Footer/Upgrade Hovered.png"), (120, 120))
event_icon = pygame.transform.scale(pygame.image.load("Assets/Footer/Event Log.png"), (120, 120))
settings_icon = pygame.transform.scale(pygame.image.load("Assets/Footer/Settings gear.png"), (120, 120))

# Buttons
button_width = x_screen / 4
button_height = y_screen / 6
button_y = y_screen - button_height

B1 = Button(0, button_y, button_width, button_height, "", Gray, GREEN, my_font, open_Bank)
B2 = Button(button_width, button_y, button_width, button_height, "", Gray, GREEN, my_font, open_Upgrade)
B3 = Button(button_width*2, button_y, button_width, button_height, "", Gray, GREEN, my_font, open_Event_Log)
B4 = Button(button_width*3, button_y, button_width, button_height, "", Gray, GREEN, my_font, open_Setting)

# Main Loop
while running:
    for event in pygame.event.get():

        # Button events
        B1.handle_event(event)
        B2.handle_event(event)
        B3.handle_event(event)
        B4.handle_event(event)

        # ESC closes all popups
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            for key in popups:
                popups[key] = False

        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg_image, (0, 0))
    screen.blit(billy_image, (500,300))
    screen.blit(title_text, title_contain)
    screen.blit(turn_text, turn_container)
    screen.blit(money_text, money_container)
    screen.blit(footer_text, footer_contain)

    # Draw buttons
    B1.draw(screen); screen.blit(bank_icon, bank_icon.get_rect(center=B1.rect.center))
    B2.draw(screen); screen.blit(upgrade_icon, upgrade_icon.get_rect(center=B2.rect.center))
    B3.draw(screen); screen.blit(event_icon, event_icon.get_rect(center=B3.rect.center))
    B4.draw(screen); screen.blit(settings_icon, settings_icon.get_rect(center=B4.rect.center))

    # --- POPUPS ---
    def draw_popup(title):
        popup_rect = pygame.Rect(300, 150, 680, 420)
        pygame.draw.rect(screen, (160,160,160), popup_rect)
        pygame.draw.rect(screen, (0,0,0), popup_rect, 4)
        txt = my_font.render(title, True, (0,0,0))
        screen.blit(txt, txt.get_rect(center=popup_rect.center))

    if popups["bank"]:       draw_popup("BANK WINDOW")
    elif popups["upgrade"]:    draw_popup("UPGRADE WINDOW")
    elif popups["event_log"]:  draw_popup("EVENT LOG")
    elif popups["settings"]:   draw_popup("SETTINGS")

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
