import pygame
from Button import Button

# Colors
RED = (255,0,0)
GREEN = (0,255,0)
GRAY = (128,128,128)

# ------------------ PYGAME SETUP ------------------
pygame.init()
pygame.display.set_caption('SmartCents')

# Base resolution for layout
BASE_W, BASE_H = 1280, 720

# Detect screen resolution automatically
info = pygame.display.Info()
x_screen, y_screen = info.current_w, info.current_h
screen = pygame.display.set_mode((x_screen, y_screen))

# Scaling factors
scale_x = x_screen / BASE_W
scale_y = y_screen / BASE_H

def scale(value, axis):
    return int(value * (scale_x if axis=='x' else scale_y))

def scale_rect(x, y, w, h):
    return pygame.Rect(scale(x,'x'), scale(y,'y'), scale(w,'x'), scale(h,'y'))

clock = pygame.time.Clock()
dt = 0
running = True

# ------------------ Freaky Images ------------------
bg_image = pygame.image.load('Assets/Background/MainBackgroundSmartCents.png')
bg_image = pygame.transform.scale(bg_image, (x_screen, y_screen))

billy_image = pygame.image.load('Assets/Background/Billy.png')
billy_image = pygame.transform.scale(billy_image, (scale(200,'x'), scale(200,'y')))

# Footer icons
bank_icon = pygame.transform.scale(pygame.image.load("Assets/Footer/Bank.png"), (scale(120,'x'), scale(120,'y')))
upgrade_icon = pygame.transform.scale(pygame.image.load("Assets/Footer/Upgrade Hovered.png"), (scale(120,'x'), scale(120,'y')))
event_icon = pygame.transform.scale(pygame.image.load("Assets/Footer/Event Log.png"), (scale(120,'x'), scale(120,'y')))
settings_icon = pygame.transform.scale(pygame.image.load("Assets/Footer/Settings gear.png"), (scale(120,'x'), scale(120,'y')))

# Upgrade icons
plot_icon     = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Plot.png"), (scale(90,'x'), scale(90,'y')))
tools_icon    = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Tools.png"), (scale(120,'x'), scale(120,'y')))
employee_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Employee.png"), (scale(80,'x'), scale(80,'y')))
potato_icon   = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Potato.png"), (scale(70,'x'), scale(70,'y')))
machine_icon  = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Tractor.png"), (scale(80,'x'), scale(80,'y')))
stall_icon    = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Stall.png"), (scale(90,'x'), scale(90,'y')))
fert_icon     = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Fertilizer.png"), (scale(90,'x'), scale(90,'y')))
chicken_icon  = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Massive Cock.png"), (scale(100,'x'), scale(100,'y')))

# ------------------ FONT ------------------
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', scale(30,'y'))

# ------------------ TEXT ------------------
title_text = my_font.render('SmartCents!', False, (0,0,0))
title_contain = title_text.get_rect(center=(scale(BASE_W/2,'x'), scale(BASE_H/20,'y')))

turn_text = my_font.render('Age: 0', False, (0,0,0))
turn_container = turn_text.get_rect(center=(scale(BASE_W/1.1,'x'), scale(BASE_H/20,'y')))

money_text = my_font.render('Money: your rich', False, (0,0,0))
money_container = money_text.get_rect(center=(scale(BASE_W/10,'x'), scale(BASE_H/20,'y')))

footer_text = my_font.render('This is a footer', False, (0,0,0))
footer_contain = footer_text.get_rect(center=(scale(BASE_W/2,'x'), scale(BASE_H/1.1,'y')))

# ------------------ Footer Popups ------------------
popups = {"bank": False, "upgrade": False, "event_log": False, "settings": False}

def open_popup(name):
    for key in popups: popups[key] = False
    popups[name] = True

def open_Bank(): open_popup("bank")
def open_Upgrade(): open_popup("upgrade")
def open_Event_Log(): open_popup("event_log")
def open_Setting(): open_popup("settings")

# ------------------ Funky Buttons ------------------
button_width  = BASE_W / 4
button_height = BASE_H / 6
button_y      = BASE_H - button_height

B1 = Button(scale(0,'x'), scale(button_y,'y'), scale(button_width,'x'), scale(button_height,'y'), "", GRAY, GREEN, my_font, open_Bank)
B2 = Button(scale(button_width,'x'), scale(button_y,'y'), scale(button_width,'x'), scale(button_height,'y'), "", GRAY, GREEN, my_font, open_Upgrade)
B3 = Button(scale(button_width*2,'x'), scale(button_y,'y'), scale(button_width,'x'), scale(button_height,'y'), "", GRAY, GREEN, my_font, open_Event_Log)
B4 = Button(scale(button_width*3,'x'), scale(button_y,'y'), scale(button_width,'x'), scale(button_height,'y'), "", GRAY, GREEN, my_font, open_Setting)

# Upgrade Icons
plot_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Plot.png"), (120, 120))
tools_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Tools.png"), (120, 120))
employee_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Employee.png"), (120, 120))
potato_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Potato.png"), (120, 120))
machine_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Tractor.png"), (120, 120))
stall_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Stall.png"), (120, 120))
fert_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Fertilizer.png"), (120, 120))
chicken_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Massive Cock.png"), (120, 120))

# Upgrade buttons
UpBut1 = Button(scale(500,'x'), scale(210,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, open_Upgrade)
UpBut2 = Button(scale(600,'x'), scale(210,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, open_Upgrade)
UpBut3 = Button(scale(700,'x'), scale(210,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, open_Upgrade)
UpBut4 = Button(scale(400,'x'), scale(350,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, open_Upgrade)
UpBut5 = Button(scale(500,'x'), scale(350,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, open_Upgrade)
UpBut6 = Button(scale(600,'x'), scale(350,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, open_Upgrade)
UpBut7 = Button(scale(700,'x'), scale(350,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, open_Upgrade)
UpBut8 = Button(scale(800,'x'), scale(350,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, open_Upgrade)
UpBut9 = Button(scale(600,'x'), scale(480,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, open_Upgrade)

# Being funky and grouping tiers and buttons
tier1_buttons = [UpBut1, UpBut2, UpBut3]
tier2_buttons = [UpBut4, UpBut5, UpBut6, UpBut7, UpBut8]
tier3_buttons = [UpBut9]

# ------------------ MAIN LOOP ------------------
def draw_tier_label(text, buttons_group):
    # Center horizontally above buttons
    min_x = min(btn.rect.left for btn in buttons_group)
    max_x = max(btn.rect.right for btn in buttons_group)
    center_x = (min_x + max_x) // 2

    # Vertical position: just above top of buttons
    top_y = min(btn.rect.top for btn in buttons_group)
    label_y = top_y - scale(20,'y')  # 20 pixels above buttons

    tier_text = my_font.render(text, True, (0,0,0))
    tier_rect = tier_text.get_rect(center=(center_x, label_y))
    screen.blit(tier_text, tier_rect)

UpBut9 = Button(600, 480, 80, 80, "T3", GRAY, GREEN, my_font, open_Upgrade)

# Bank Buttons
Deposit_Button = Button(500,210, 100,50, "Deposit", GRAY, GREEN, my_font, None)
Withdrawl_Button = Button(700, 210, 100, 50, "Withdrawl", GRAY, GREEN, my_font, None)
Input_Box = pygame.rect.Rect(550, 310, 200, 50)

text = ""
saved = ""

# Main Loop
while running:
    for event in pygame.event.get():
        # Button events
        B1.handle_event(event)
        B2.handle_event(event)
        B3.handle_event(event)
        B4.handle_event(event)
        for btn in [UpBut1, UpBut2, UpBut3, UpBut4, UpBut5, UpBut6, UpBut7, UpBut8, UpBut9]:
            btn.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            for key in popups:
                popups[key] = False
        
        if popups["bank"] and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                saved = text
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode

        if event.type == pygame.QUIT:
            running = False

    # ------------------ DRAWING QWERTY ------------------
    screen.blit(bg_image, (0,0))
    screen.blit(billy_image, (scale(500,'x'), scale(300,'y')))
    screen.blit(title_text, title_contain)
    screen.blit(turn_text, turn_container)
    screen.blit(money_text, money_container)
    screen.blit(footer_text, footer_contain)

    # Draw footer buttons + icons
    for btn, icon in zip([B1,B2,B3,B4], [bank_icon, upgrade_icon, event_icon, settings_icon]):
        btn.draw(screen)
        screen.blit(icon, icon.get_rect(center=btn.rect.center))

    # ------------------ Popup on screen?? ------------------
    def draw_popup():
        popup_rect = scale_rect(300,150,680,420)
        pygame.draw.rect(screen, (160,160,160), popup_rect)
        pygame.draw.rect(screen, (0,0,0), popup_rect, 4)

    def draw_bank():
        Deposit_Button.draw(screen)
        Withdrawl_Button.draw(screen)
        pygame.draw.rect(screen, (255,255,255), Input_Box, 50)
        screen.blit(my_font.render(text, True, (0,0,0)), (Input_Box.x+10, Input_Box.y+10))

    if popups["bank"]:       draw_popup(); draw_bank()
    elif popups["upgrade"]:    draw_popup(); draw_upgrades()
    elif popups["event_log"]:  draw_popup()
    elif popups["settings"]:   draw_popup()
    
    def draw_upgrades():
        # Draw tier labels
        draw_tier_label("Tier 1!", tier1_buttons)
        draw_tier_label("Tier 2!", tier2_buttons)
        draw_tier_label("Tier 3!", tier3_buttons)
        icons = [plot_icon, tools_icon, employee_icon, plot_icon, potato_icon, machine_icon, stall_icon, fert_icon, chicken_icon]
        buttons = [UpBut1, UpBut2, UpBut3, UpBut4, UpBut5, UpBut6, UpBut7, UpBut8, UpBut9]
        for btn, icon in zip(buttons, icons):
            btn.draw(screen)
            pygame.draw.rect(screen, (0,0,0), btn.rect, 3)
            screen.blit(icon, icon.get_rect(center=btn.rect.center))

    if popups["bank"]: draw_popup()
    elif popups["upgrade"]: draw_popup(); draw_upgrades()
    elif popups["event_log"]: draw_popup()
    elif popups["settings"]: draw_popup()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
