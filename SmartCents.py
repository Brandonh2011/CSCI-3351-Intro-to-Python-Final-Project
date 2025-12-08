import pygame
from Button import Button
from turn import TurnSystem
from events import trigger_event
from summary import generate_summary, enable_summary_access

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

# ------------------ FONT ------------------
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', scale(30,'y'))

# ------------------ GAME LOGIC ------------------
# Initialize game
game = TurnSystem()
enable_summary_access()  # Allow summary generation

# Game state variables
current_event_message = ""
game_over = False
game_won = False
game_summary = ""
event_popup_active = False
current_event_data = None
upgrade_message = ""  # For showing upgrade purchase feedback
upgrade_message_timer = 0  # Timer to hide message

# Event log to track all events that have occurred
event_log = []  # List of (event_name, result_text) tuples

# Win objective
WIN_GOAL = 50000  # $50,000 net worth

# ------------------ GAME END SCREENS ------------------
def draw_game_over():
    overlay = pygame.Surface((x_screen, y_screen))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Game over box
    game_over_rect = scale_rect(200, 100, 880, 520)
    pygame.draw.rect(screen, (200, 200, 200), game_over_rect)
    pygame.draw.rect(screen, (0, 0, 0), game_over_rect, 4)

    # Title
    title_font = pygame.font.SysFont('Comic Sans MS', scale(50,'y'))
    title_text = title_font.render("GAME OVER", True, (255, 0, 0))
    title_rect = title_text.get_rect(center=(x_screen//2, scale(150,'y')))
    screen.blit(title_text, title_rect)

    # Get current player stats for display
    money = game.player.getMoney()
    savings = game.player.bank.getSavings()
    year = game.player.getYear()
    networth = money + savings

    # Display current balance information
    small_font = pygame.font.SysFont('Comic Sans MS', scale(20,'y'))

    balance_text = small_font.render(f"Checking Balance: ${money:.0f}", True, (0, 0, 0))
    balance_rect = balance_text.get_rect(center=(x_screen//2, scale(200,'y')))
    screen.blit(balance_text, balance_rect)

    savings_text = small_font.render(f"Savings Balance: ${savings:.0f}", True, (0, 0, 0))
    savings_rect = savings_text.get_rect(center=(x_screen//2, scale(230,'y')))
    screen.blit(savings_text, savings_rect)

    networth_text = small_font.render(f"Total Net Worth: ${networth:.0f}", True, (0, 0, 0))
    networth_rect = networth_text.get_rect(center=(x_screen//2, scale(260,'y')))
    screen.blit(networth_text, networth_rect)

    years_text = small_font.render(f"Years Survived: {year}", True, (0, 0, 0))
    years_rect = years_text.get_rect(center=(x_screen//2, scale(290,'y')))
    screen.blit(years_text, years_rect)

    # Game over message
    game_over_msg = small_font.render("BANKRUPTCY - Game Over!", True, (255, 0, 0))
    msg_rect = game_over_msg.get_rect(center=(x_screen//2, scale(330,'y')))
    screen.blit(game_over_msg, msg_rect)

    # Play Again button
    play_again_button_rect = pygame.Rect(x_screen//2 - scale(75,'x'), scale(450,'y'), scale(150,'x'), scale(40,'y'))
    pygame.draw.rect(screen, GREEN, play_again_button_rect)
    pygame.draw.rect(screen, (0, 0, 0), play_again_button_rect, 2)
    play_again_text = small_font.render("Play Again", True, (255, 255, 255))
    play_again_text_rect = play_again_text.get_rect(center=play_again_button_rect.center)
    screen.blit(play_again_text, play_again_text_rect)

    # Handle Play Again button click
    if event.type == pygame.MOUSEBUTTONDOWN and play_again_button_rect.collidepoint(event.pos):
        reset_game()

def draw_win_screen():
    overlay = pygame.Surface((x_screen, y_screen))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Win box
    win_rect = scale_rect(200, 100, 880, 520)
    pygame.draw.rect(screen, (200, 200, 200), win_rect)
    pygame.draw.rect(screen, (0, 0, 0), win_rect, 4)

    # Title
    title_font = pygame.font.SysFont('Comic Sans MS', scale(50,'y'))
    title_text = title_font.render("CONGRATULATIONS!", True, (0, 150, 0))
    title_rect = title_text.get_rect(center=(x_screen//2, scale(150,'y')))
    screen.blit(title_text, title_rect)

    # Subtitle
    subtitle_font = pygame.font.SysFont('Comic Sans MS', scale(30,'y'))
    subtitle_text = subtitle_font.render("You Won the Game!", True, (0, 100, 0))
    subtitle_rect = subtitle_text.get_rect(center=(x_screen//2, scale(200,'y')))
    screen.blit(subtitle_text, subtitle_rect)

    # Summary text
    small_font = pygame.font.SysFont('Comic Sans MS', scale(20,'y'))
    lines = game_summary.split('\n')
    y_offset = scale(250,'y')
    for line in lines:
        if line.strip():  # Skip empty lines
            text_surface = small_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x_screen//2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += scale(25,'y')

    # Play Again button
    play_again_button_rect = pygame.Rect(x_screen//2 - scale(75,'x'), scale(40,'y'), scale(150,'x'), scale(40,'y'))
    pygame.draw.rect(screen, GREEN, play_again_button_rect)
    pygame.draw.rect(screen, (0, 0, 0), play_again_button_rect, 2)
    play_again_text = small_font.render("Play Again", True, (255, 255, 255))
    play_again_text_rect = play_again_text.get_rect(center=play_again_button_rect.center)
    screen.blit(play_again_text, play_again_text_rect)

    # Handle Play Again button click
    if event.type == pygame.MOUSEBUTTONDOWN and play_again_button_rect.collidepoint(event.pos):
        reset_game()

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
def quit_game():
    global running
    running = False

def reset_game():
    global game, current_event_message, game_over, game_won, game_summary, event_popup_active, current_event_data, upgrade_message, upgrade_message_timer

    # Reset all game state
    game = TurnSystem()  # Create new game instance
    enable_summary_access()  # Allow summary generation

    # Reset game state variables
    current_event_message = ""
    game_over = False
    game_won = False
    game_summary = ""
    event_popup_active = False
    current_event_data = None
    upgrade_message = ""
    upgrade_message_timer = 0

    # Close any open popups
    for key in popups:
        popups[key] = False

    # Reinitialize display text
    update_display_text()

# Upgrade purchase functions
def purchase_upgrade_1(): purchase_upgrade("land_increase_1")
def purchase_upgrade_2(): purchase_upgrade("hand_tools")
def purchase_upgrade_3(): purchase_upgrade("Employee")
def purchase_upgrade_4(): purchase_upgrade("land_increase_2")
def purchase_upgrade_5(): purchase_upgrade("potato_crops")
def purchase_upgrade_6(): purchase_upgrade("Machinery")
def purchase_upgrade_7(): purchase_upgrade("farmers_market_stall")
def purchase_upgrade_8(): purchase_upgrade("fertilizerConsumable")
def purchase_upgrade_9(): purchase_upgrade("chicken")

def purchase_upgrade(upgrade_key):
    global upgrade_message, upgrade_message_timer
    success, message = game.upgrades.purchaseUpgrade(upgrade_key, game.player)
    upgrade_message = message
    upgrade_message_timer = 180  # Show message for 3 seconds (60 FPS * 3)
    if success:
        update_display_text()

# ------------------ Funky Buttons ------------------
button_width  = BASE_W / 4
button_height = BASE_H / 6
button_y      = BASE_H - button_height

B1 = Button(scale(0,'x'), scale(button_y,'y'), scale(button_width,'x'), scale(button_height,'y'), "", GRAY, GREEN, my_font, open_Bank)
B2 = Button(scale(button_width,'x'), scale(button_y,'y'), scale(button_width,'x'), scale(button_height,'y'), "", GRAY, GREEN, my_font, open_Upgrade)
B3 = Button(scale(button_width*2,'x'), scale(button_y,'y'), scale(button_width,'x'), scale(button_height,'y'), "", GRAY, GREEN, my_font, open_Event_Log)
B4 = Button(scale(button_width*3,'x'), scale(button_y,'y'), scale(button_width,'x'), scale(button_height,'y'), "", GRAY, GREEN, my_font, quit_game)

# Upgrade Icons
plot_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Plot.png"), (120, 120))
tools_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Tools.png"), (120, 120))
employee_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Employee.png"), (120, 120))
potato_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Potato.png"), (120, 120))
machine_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Tractor.png"), (120, 120))
stall_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Stall.png"), (120, 120))
fert_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Fertilizer.png"), (120, 120))
chicken_icon = pygame.transform.scale(pygame.image.load("Assets/Upgrade Assets/Massive Cock.png"), (120, 120))

# Upgrade buttons - repositioned for better spacing in expanded popup
UpBut1 = Button(scale(500,'x'), scale(220,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, purchase_upgrade_1)
UpBut2 = Button(scale(600,'x'), scale(220,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, purchase_upgrade_2)
UpBut3 = Button(scale(700,'x'), scale(220,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, purchase_upgrade_3)
UpBut4 = Button(scale(400,'x'), scale(400,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, purchase_upgrade_4)
UpBut5 = Button(scale(500,'x'), scale(400,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, purchase_upgrade_5)
UpBut6 = Button(scale(600,'x'), scale(400,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, purchase_upgrade_6)
UpBut7 = Button(scale(700,'x'), scale(400,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, purchase_upgrade_7)
UpBut8 = Button(scale(800,'x'), scale(400,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, purchase_upgrade_8)
UpBut9 = Button(scale(600,'x'), scale(580,'y'), scale(80,'x'), scale(80,'y'), "", GRAY, GREEN, my_font, purchase_upgrade_9)

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

    # Vertical position: above buttons but not too high to be visible
    top_y = min(btn.rect.top for btn in buttons_group)
    label_y = top_y - scale(45,'y')  # 45 pixels above buttons for better visibility

    # Use readable font for tier labels
    tier_font = pygame.font.SysFont('Comic Sans MS', scale(26,'y'))
    tier_text = tier_font.render(text, True, (0, 0, 0))
    tier_rect = tier_text.get_rect(center=(center_x, label_y))
    screen.blit(tier_text, tier_rect)

def next_turn():
    global current_event_message, game_over, game_won, game_summary, event_popup_active, current_event_data
    if not game_over and not game_won:
        # Process turn
        turn_result = game.oneTurn()

        # Check for game over
        if turn_result.get("status") == "Bankrupt":
            game_over = True
            game_summary = generate_summary(game.player)
            update_display_text()  # Update display to match game over balance
            return

        # Check for win condition (net worth >= $50,000)
        net_worth = game.player.getMoney() + game.player.bank.getSavings()
        if net_worth >= 50000:
            game_won = True
            game_summary = generate_summary(game.player)
            return

        # Trigger random event
        event_result = trigger_event(game.player, game.upgrades)
        current_event_message = f"{event_result['event_name']}: {event_result['result']}"
        current_event_data = event_result
        event_popup_active = True  # Show event popup

        # Add event to the event log
        event_log.append((event_result['event_name'], event_result['result']))

        # Update display text
        update_display_text()

def update_display_text():
    global turn_text, money_text, footer_text

    year = game.player.getYear()
    money = game.player.getMoney()
    savings = game.player.bank.getSavings()
    happiness = game.player.getHappiness()
    base_income = game.upgrades.calculateIncome()

    turn_text = my_font.render(f'Year: {year}', False, (0,0,0))
    money_text = my_font.render(f'Checking: ${money:.0f} | Savings: ${savings:.0f}', False, (0,0,0))
    footer_text = my_font.render(f'Income: ${base_income:.0f}/turn | Happiness: {happiness} | {current_event_message}', False, (0,0,0))

# Next Turn Button 
next_turn_button = Button(scale(BASE_W - 250,'x'), scale(BASE_H/10,'y'), scale(200,'x'), scale(50,'y'), "Next Turn", GRAY, GREEN, my_font, next_turn)

# Initialize display text
update_display_text()
# Bank Buttons
Deposit_Button = Button(500,210, 275, 50, "Deposit", GRAY, GREEN, my_font, None)
Withdrawl_Button = Button(700, 210, 275, 50, "Withdrawl", GRAY, GREEN, my_font, None)
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

        # Upgrade buttons - handle when upgrade popup is open
        if popups["upgrade"]:
            UpBut1.handle_event(event)
            UpBut2.handle_event(event)
            UpBut3.handle_event(event)
            UpBut4.handle_event(event)
            UpBut5.handle_event(event)
            UpBut6.handle_event(event)
            UpBut7.handle_event(event)
            UpBut8.handle_event(event)
            UpBut9.handle_event(event)

        # Next turn button - handled by button action
        if not game_over and not game_won:
            next_turn_button.handle_event(event)



        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            for key in popups:
                popups[key] = False
        
        # Bank popup handling
        if popups["bank"]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Deposit_Button.rect.collidepoint(event.pos) and text:
                    try:
                        amount = float(text)
                        result = game.deposit_to_savings(amount)
                        update_display_text()
                        text = ""  # Clear input
                    except ValueError:
                        text = ""  # Clear invalid input

                elif Withdrawl_Button.rect.collidepoint(event.pos) and text:
                    try:
                        amount = float(text)
                        result = game.withdraw_from_savings(amount)
                        update_display_text()
                        text = ""  # Clear input
                    except ValueError:
                        text = ""  # Clear invalid input

            if event.type == pygame.KEYDOWN:
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

    # Draw next turn button (only if game not over and not won)
    if not game_over and not game_won:
        next_turn_button.draw(screen)

    # Draw income and win objective progress (only if game not over and not won)
    if not game_over and not game_won:
        # Show base income per turn 
        base_income = game.upgrades.calculateIncome()
        income_text = f"Income per turn: ${base_income:.0f}"
        income_font = pygame.font.SysFont('Comic Sans MS', scale(28,'y'))
        income_surface = income_font.render(income_text, True, (0, 100, 0))  # Green for income
        income_rect = income_surface.get_rect(center=(x_screen//2, scale(BASE_H/6,'y')))
        screen.blit(income_surface, income_rect)

        # Show win objective progress
        net_worth = game.player.getMoney() + game.player.bank.getSavings()
        progress_text = f"Win Goal: ${net_worth:.0f} / ${WIN_GOAL:.0f}"
        progress_color = GREEN if net_worth >= WIN_GOAL else (0, 0, 0)
        progress_font = pygame.font.SysFont('Comic Sans MS', scale(25,'y'))
        progress_surface = progress_font.render(progress_text, True, progress_color)
        progress_rect = progress_surface.get_rect(center=(x_screen//2, scale(BASE_H/8,'y')))
        screen.blit(progress_surface, progress_rect)

    # Draw upgrade message if active
    if upgrade_message and upgrade_message_timer > 0:
        message_font = pygame.font.SysFont('Comic Sans MS', scale(24,'y'))
        message_color = GREEN if "Purchased" in upgrade_message or "Hired" in upgrade_message else RED
        message_text = message_font.render(upgrade_message, True, message_color)
        message_rect = message_text.get_rect(center=(x_screen//2, scale(BASE_H - 100,'y')))
        screen.blit(message_text, message_rect)
        upgrade_message_timer -= 1  # Countdown timer
    elif upgrade_message_timer <= 0:
        upgrade_message = ""  # Clear message when timer expires

# ------------------ Popup on screen?? ------------------
    def draw_popup():
        popup_rect = scale_rect(300,120,680,600)  # Increased height from 420 to 600 and moved up slightly
        pygame.draw.rect(screen, (160,160,160), popup_rect)
        pygame.draw.rect(screen, (0,0,0), popup_rect, 4)

        # Draw close button (X)
        close_button_rect = pygame.Rect(popup_rect.right - scale(30,'x'), popup_rect.top + scale(10,'y'), scale(20,'x'), scale(20,'y'))
        pygame.draw.rect(screen, RED, close_button_rect)
        close_text = my_font.render("X", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=close_button_rect.center)
        screen.blit(close_text, close_text_rect)

        # Handle close button click
        if event.type == pygame.MOUSEBUTTONDOWN and close_button_rect.collidepoint(event.pos):
            for key in popups:
                popups[key] = False

        return popup_rect

    def draw_event_log():
        popup_rect = draw_popup()  # get popup rect

        # Title
        title_font = pygame.font.SysFont('Comic Sans MS', scale(32,'y'))
        title_text = title_font.render("Event History", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(popup_rect.centerx, popup_rect.top + scale(40,'y')))
        screen.blit(title_text, title_rect)

        # Display events from most recent to oldest
        event_font = pygame.font.SysFont('Comic Sans MS', scale(16,'y'))
        y_offset = popup_rect.top + scale(80,'y')
        max_events_to_show = 12  # Limit to prevent overflow

        # Reverse the event log to show most recent first
        events_to_display = event_log[-max_events_to_show:][::-1]

        for event_name, event_result in events_to_display:
            if y_offset > popup_rect.bottom - scale(60,'y'):  # Leave space for close button
                break

            # Event name in bold/different color
            event_name_text = event_font.render(f"{event_name}:", True, (0, 0, 150))
            event_name_rect = event_name_text.get_rect(left=popup_rect.left + scale(20,'x'), top=y_offset)
            screen.blit(event_name_text, event_name_rect)

            # Event result - color based on positive/negative
            loss_keywords = ["cost you", "took a hit", "lost", "paid an extra", "missed out", "medical bill", "investment loss", "tax increase"]
            is_negative = any(keyword in event_result.lower() for keyword in loss_keywords)
            result_color = (255, 0, 0) if is_negative else (0, 100, 0)

            event_result_text = event_font.render(event_result, True, result_color)
            event_result_rect = event_result_text.get_rect(left=popup_rect.left + scale(30,'x'), top=y_offset + scale(18,'y'))
            screen.blit(event_result_text, event_result_rect)

            y_offset += scale(40,'y')  # Space between events

        # If no events yet
        if not event_log:
            no_events_text = event_font.render("No events have occurred yet.", True, (100, 100, 100))
            no_events_rect = no_events_text.get_rect(center=(popup_rect.centerx, popup_rect.centery))
            screen.blit(no_events_text, no_events_rect)

    def draw_bank():

        popup_rect = draw_popup()  # get popup rect

        # Horizontal center
        center_x = popup_rect.centerx
        start_y = popup_rect.top + scale(60,'y')  # some padding from top

        # Buttons: place side by side
        spacing = scale(150,'x')
        Deposit_Button.rect.center = (center_x - spacing//2, start_y)
        Withdrawl_Button.rect.center = (center_x + spacing//2, start_y)

        # Input box: below buttons
        Input_Box.center = (center_x, start_y + scale(80,'y'))

        Deposit_Button.draw(screen)
        Withdrawl_Button.draw(screen)
        pygame.draw.rect(screen, (255,255,255), Input_Box, 50)
        screen.blit(my_font.render(text, True, (0,0,0)), (Input_Box.x+10, Input_Box.y+10))

    # Draw popups
    if popups["bank"]:
        draw_popup()
        draw_bank()
    elif popups["upgrade"]:
        draw_popup()
        draw_upgrades()
    elif popups["event_log"]:
        draw_popup()
        draw_event_log()
    elif popups["settings"]:
        draw_popup()
       

    # Draw event popup (can appear over other popups)
    if event_popup_active:
        draw_event_popup()
    
    def draw_event_popup():
        global event_popup_active
        if not current_event_data:
            return

        
        overlay = pygame.Surface((x_screen, y_screen))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Event popup box
        popup_rect = scale_rect(250, 200, 780, 320)
        pygame.draw.rect(screen, (200, 200, 200), popup_rect)
        pygame.draw.rect(screen, (0, 0, 0), popup_rect, 4)

        # Event title
        title_font = pygame.font.SysFont('Comic Sans MS', scale(36,'y'))
        title_text = title_font.render(current_event_data['event_name'], True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(x_screen//2, scale(250,'y')))
        screen.blit(title_text, title_rect)

        # Event description
        desc_font = pygame.font.SysFont('Comic Sans MS', scale(24,'y'))
        desc_text = desc_font.render(current_event_data['description'], True, (0, 0, 0))
        desc_rect = desc_text.get_rect(center=(x_screen//2, scale(300,'y')))
        screen.blit(desc_text, desc_rect)

        # Event result - color based on positive/negative
        result_font = pygame.font.SysFont('Comic Sans MS', scale(28,'y'))

        # Determine if event is negative (loses money) by checking result text for loss indicators
        result_text_content = current_event_data['result']
        loss_keywords = ["cost you", "took a hit", "lost", "paid an extra", "missed out", "medical bill", "investment loss", "tax increase"]
        is_negative = any(keyword in result_text_content.lower() for keyword in loss_keywords)
        result_color = (255, 0, 0) if is_negative else (0, 100, 0)  # Red for negative, green for positive

        result_text = result_font.render(result_text_content, True, result_color)
        result_rect = result_text.get_rect(center=(x_screen//2, scale(350,'y')))
        screen.blit(result_text, result_rect)

        # OK button
        ok_button_rect = pygame.Rect(x_screen//2 - scale(50,'x'), scale(420,'y'), scale(100,'x'), scale(40,'y'))
        pygame.draw.rect(screen, GREEN, ok_button_rect)
        pygame.draw.rect(screen, (0, 0, 0), ok_button_rect, 2)
        ok_text = my_font.render("OK", True, (255, 255, 255))
        ok_text_rect = ok_text.get_rect(center=ok_button_rect.center)
        screen.blit(ok_text, ok_text_rect)

        # Handle OK button click
        if event.type == pygame.MOUSEBUTTONDOWN and ok_button_rect.collidepoint(event.pos):
            event_popup_active = False

    def draw_upgrades():
        # Draw tier labels
        draw_tier_label("Tier 1!", tier1_buttons)
        draw_tier_label("Tier 2!", tier2_buttons)
        draw_tier_label("Tier 3!", tier3_buttons)

        upgrade_keys = ["land_increase_1", "hand_tools", "Employee", "land_increase_2", "potato_crops", "Machinery", "farmers_market_stall", "fertilizerConsumable", "chicken"]
        icons = [plot_icon, tools_icon, employee_icon, plot_icon, potato_icon, machine_icon, stall_icon, fert_icon, chicken_icon]
        buttons = [UpBut1, UpBut2, UpBut3, UpBut4, UpBut5, UpBut6, UpBut7, UpBut8, UpBut9]

        small_font = pygame.font.SysFont('Comic Sans MS', scale(16,'y'))

        for i, (btn, icon, key) in enumerate(zip(buttons, icons, upgrade_keys)):
            btn.draw(screen)
            pygame.draw.rect(screen, (0,0,0), btn.rect, 3)
            screen.blit(icon, icon.get_rect(center=btn.rect.center))

            # Get upgrade info
            upgrade = game.upgrades.upgrades[key]

            # Handle fertilizerConsumable 
            if key == "fertilizerConsumable":
                cost = upgrade["cost"]
                # Display cost below button
                cost_text = small_font.render(f"${cost}", True, (0, 0, 0))
                cost_rect = cost_text.get_rect(center=(btn.rect.centerx, btn.rect.bottom + scale(20,'y')))
                screen.blit(cost_text, cost_rect)

                # Display "Consumable" instead of level
                level_text = small_font.render("Consumable", True, (0, 0, 0))
                level_rect = level_text.get_rect(center=(btn.rect.centerx, btn.rect.bottom + scale(40,'y')))
                screen.blit(level_text, level_rect)
            else:
                # Regular upgrade with levels
                current_level = upgrade["current_level"]
                max_level = upgrade["max_level"]

                if current_level >= max_level:
                    # Maxed out - show "Maxed" instead of price
                    cost_text = small_font.render("Maxed", True, (0, 100, 0))  # Green for maxed
                    cost_rect = cost_text.get_rect(center=(btn.rect.centerx, btn.rect.bottom + scale(30,'y')))
                    screen.blit(cost_text, cost_rect)
                else:
                    # Not maxed - show next purchase cost and level
                    cost = upgrade["cost"] * (upgrade["current_level"] + 1)  # Cost scales with level

                    # Display cost below button
                    cost_text = small_font.render(f"${cost}", True, (0, 0, 0))
                    cost_rect = cost_text.get_rect(center=(btn.rect.centerx, btn.rect.bottom + scale(20,'y')))
                    screen.blit(cost_text, cost_rect)

                    # Display level info
                    level_text = small_font.render(f"{current_level}/{max_level}", True, (0, 0, 0))
                    level_rect = level_text.get_rect(center=(btn.rect.centerx, btn.rect.bottom + scale(40,'y')))
                    screen.blit(level_text, level_rect)

    # Draw game over or win screen
    if game_over:
        draw_game_over()
    elif game_won:
        draw_win_screen()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
