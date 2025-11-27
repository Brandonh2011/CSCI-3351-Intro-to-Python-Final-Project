import random  

class Event:
    def __init__(self, name, description, effect):
        self.name = name              # Name of the event (e.g., "Medical Bill")
        self.description = description  # Short summary of what happens
        self.effect = effect            # Function that applies the event’s impact

    def apply(self, player):
        # Execute the event’s effect on the given player object.
        return self.effect(player)


#            Individual Event Effects

def medical_bill_effect(player):
    cost = random.randint(400, 1000)
    player.minusMoney(cost)
    player.minusHappiness(5)
    return f"You were hit with a medical bill of ${cost}."

def investment_loss_effect(player):
    loss_amount = random.randint(800, 2000)
    player.minusMoney(loss_amount)         
    player.minusHappiness(10)
    return f"You lost money on investments this year and took a hit of ${loss_amount}."

def tax_increase_effect(player):
    tax_cost = random.randint(150, 400)
    player.minusMoney(tax_cost)
    return f"The government increased taxes. You paid an extra ${tax_cost}."

def stock_boom_effect(player):
    gain = random.randint(400, 1200)  
    player.addMoney(gain)
    player.addHappiness(5)
    return f"The stock market boomed! You gained ${gain}."

def business_bonus_effect(player):
    bonus = random.randint(300, 1000)  
    player.addMoney(bonus)
    player.addHappiness(5)
    return f"Your business had a strong year! Bonus income: ${bonus}."



#                   Event Pool 
# Dictionary mapping event keys to Event objects
EVENT_POOL = {
    "medical_bill": Event(
        "Medical Bill",
        "Unexpected medical expenses hit you hard.",
        medical_bill_effect
    ),
    "job_loss": Event(
        "Job Loss",
        "You struggled with income this year.",
        investment_loss_effect
    ),
    "tax_increase": Event(
        "Tax Increase",
        "Government policy change increased taxes.",
        tax_increase_effect
    ),
    "stock_boom": Event(
        "Stock Market Boom",
        "Your investments paid off big time.",
        stock_boom_effect
    ),
    "business_bonus": Event(
        "Business Bonus",
        "Your farm has performed exceptionally well.",
        business_bonus_effect
    )
}


#           Event Chances of happening
# Higher percentages mean higher chance of that event happening
EVENT_PERCENTAGES = {
    "medical_bill": 0.12,
    "investment_loss": 0.10,
    "tax_increase": 0.13,
    "stock_boom": 0.32,
    "business_bonus": 0.33
}


def get_random_event():
    
   # Randomly select one event from EVENT_POOL based on EVENT_PERCENTAGES.
    # Returns the selected Event object.
    
    names = list(EVENT_PERCENTAGES.keys())       # Event identifiers
    percentages = list(EVENT_PERCENTAGES.values())   # Corresponding probabilities
    selected = random.choices(names, weights=percentages, k=1)[0]  # Pick one key
    return EVENT_POOL[selected]              # Return the matching Event object


def trigger_event(player):
    
    # Selects and applies a random event to the player.
    # Returns a dictionary summarizing the event and its result text.

    event = get_random_event()               # Pick a random event
    result_text = event.apply(player)        # Apply the event’s effect
    return {
        "event_name": event.name,
        "description": event.description,
        "result": result_text
    }

if __name__ == "__main__":
    print("\nSorry, but events.py can only be imported!")