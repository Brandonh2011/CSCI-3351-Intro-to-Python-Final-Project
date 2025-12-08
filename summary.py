# summary.py
# This file creates the final SmartCents report. Only main.py is allowed to run it.

from player import Player          # Access player info  :contentReference[oaicite:0]{index=0}
from turn import TurnSystem        # Used so main.py can pass game state  :contentReference[oaicite:1]{index=1}

# Access lock so players can't run this file directly
_ALLOWED = False


# Enables summary generation — only main.py should call this
def enable_summary_access():
    global _ALLOWED
    _ALLOWED = True


# Builds and returns the final SmartCents summary text
def generate_summary(player: Player):

    # Block running summary.py directly unless main.py activates it
    if not _ALLOWED:
        raise PermissionError("summary.py must be executed through main.py")

    # Gather all the player's final stats
    name = player.getName()
    money = player.getMoney()
    savings = player.bank.getSavings()
    happiness = player.getHappiness()
    year = player.getYear()

    # Net worth is the total of checking + savings
    networth = money + savings

    # Determine the ending message based on final conditions
    if player.isBankrupt():
        ending = "GAME OVER — BANKRUPT"
    elif happiness <= 0:
        ending = "GAME OVER — UNHAPPY"
    else:
        ending = "CONGRATULATIONS — YOU COMPLETED SMARTCENTS!"

    # Create the formatted report text
    
    #--- WELL-BEING SUMMARY --- put back on line 58/59 if we want it for future
#Happiness Level:       {happiness}
    summary_text = f"""
===========================
   SMARTCENTS FINAL REPORT
===========================

Player: {name}
Years Survived: {year}

--- FINANCIAL SUMMARY ---
Checking Balance:     ${money:.0f}
Savings Balance:      ${savings:.0f}
Total Net Worth:      ${networth:.0f}



--- FINAL RESULT ---
{ending}

===========================
Thank you for playing!
===========================
"""

    return summary_text


# Prevent users from opening this file directly
if __name__ == "__main__":
    raise RuntimeError("summary.py cannot be run alone — use main.py")
