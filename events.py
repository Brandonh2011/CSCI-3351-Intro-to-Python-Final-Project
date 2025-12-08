import random  

class Event:
    def __init__(self, name, description, effect, requires_upgrades=False):
        self.name = name              
        self.description = description  
        self.effect = effect            
        self.requires_upgrades = requires_upgrades  # Whether this event needs upgrade context

    def apply(self, player, game_upgrades=None):
        # Execute the event’s effect on the given player object.
        if self.requires_upgrades:
            return self.effect(player, game_upgrades)
        else:
            return self.effect(player)


#Individual Event Effects

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

#Strategic Event Effects

def emergency_fund_bonus_effect(player):
    savings = player.bank.getSavings()
    if savings >= 2000:
        bonus = int(savings * 0.1)  # 10% of savings as bonus
        player.addMoney(bonus)
        player.addHappiness(3)
        return f"Your emergency fund paid off! You earned ${bonus} in interest."
    else:
        cost = random.randint(300, 1200)
        player.minusMoney(cost)
        player.minusHappiness(8)
        return f"You had an emergency but not enough savings! Cost you ${cost}."

def upgrade_maintenance_crisis_effect(player, game_upgrades):
    # Maintanence issues if player has multiple complementary upgrades 
    tool_level = game_upgrades.upgrades["hand_tools"]["current_level"]
    machine_level = game_upgrades.upgrades["Machinery"]["current_level"]
    land_level = game_upgrades.upgrades["land_increase_1"]["current_level"] + game_upgrades.upgrades["land_increase_2"]["current_level"]

    upgrade_count = tool_level + machine_level + land_level

    if upgrade_count >= 3:
        maintenance_cost = upgrade_count * 400
        player.minusMoney(maintenance_cost)
        player.minusHappiness(12)
        return f"Multiple upgrades caused maintenance nightmare! Emergency repairs cost ${maintenance_cost}."
    else:
        cost = random.randint(300, 600)
        player.minusMoney(cost)
        player.minusHappiness(6)
        return f"Equipment maintenance issues cost you ${cost}."

def savings_devaluation_crisis_effect(player):
    savings = player.bank.getSavings()
    if savings >= 5000:
        devaluation_loss = int(savings * 0.20)  # 20% devaluation
        player.minusMoney(devaluation_loss)
        player.minusHappiness(15)
        return f"Economic crisis! Your savings lost ${devaluation_loss} in value due to inflation."
    elif savings >= 2000:
        devaluation_loss = int(savings * 0.15)  # 15% devaluation
        player.minusMoney(devaluation_loss)
        player.minusHappiness(10)
        return f"Inflation hit hard! Lost ${devaluation_loss} from your savings."
    elif savings >= 500:
        devaluation_loss = int(savings * 0.10)  # 10% devaluation
        player.minusMoney(devaluation_loss)
        player.minusHappiness(8)
        return f"Market volatility affected your savings. Lost ${devaluation_loss}."
    else:
        player.minusHappiness(5)
        return "Your lack of savings left you vulnerable to economic uncertainty."

def equipment_warning_effect(player, game_upgrades):
    year = player.getYear()
    if year >= 5 and game_upgrades.upgrades["Machinery"]["current_level"] == 0:
        player.minusHappiness(5)
        return "Your equipment is getting old. Consider upgrading machinery soon."
    elif year >= 3 and game_upgrades.upgrades["hand_tools"]["current_level"] == 0:
        player.minusHappiness(3)
        return "Your basic tools are wearing out. Hand tools upgrade recommended."
    else:
        player.addHappiness(2)
        return "Your equipment is in good condition."

def labor_dispute_crisis_effect(player, game_upgrades):
    employee_count = game_upgrades.upgrades["Employee"]["current_level"]
    if employee_count > 0:
        dispute_cost = employee_count * 700  
        player.minusMoney(dispute_cost)
        player.minusHappiness(12)
        return f"Labor dispute! Strikes and settlements cost you ${dispute_cost}."
    else:
        cost = random.randint(400, 800)
        player.minusMoney(cost)
        player.minusHappiness(8)
        return f"Contract labor issues cost you ${cost} in delays and replacements."

def market_demand_shift_effect(player, game_upgrades):
    # Bonus if player has market stall upgrade
    has_market = game_upgrades.upgrades["farmers_market_stall"]["current_level"] > 0
    has_potatoes = game_upgrades.upgrades["potato_crops"]["current_level"] > 0

    if has_market and has_potatoes:
        bonus = random.randint(800, 1500)
        player.addMoney(bonus)
        player.addHappiness(6)
        return f"Market demand for potatoes is high! Sold out for ${bonus}."
    elif has_market:
        bonus = random.randint(400, 800)
        player.addMoney(bonus)
        player.addHappiness(3)
        return f"Your market stall helped during demand shift. Extra sales: ${bonus}."
    else:
        loss = random.randint(200, 500)
        player.minusMoney(loss)
        player.minusHappiness(4)
        return f"Market demand shifted but you missed out. Lost potential sales: ${loss}."

def diversification_bonus_effect(player, game_upgrades):
    # Bonus for having multiple income sources
    income_sources = 0
    if game_upgrades.upgrades["potato_crops"]["current_level"] > 0:
        income_sources += 1
    if game_upgrades.upgrades["chicken"]["current_level"] > 0:
        income_sources += 1
    if player.bank.getSavings() >= 2000:
        income_sources += 1  # Savings as income source

    if income_sources >= 2:
        bonus = income_sources * 300
        player.addMoney(bonus)
        player.addHappiness(4)
        return f"Your diversified income sources paid off! Stability bonus: ${bonus}."
    else:
        return "Consider diversifying your income sources for stability."



#Event Pool
# Dictionary mapping event keys to Event objects
EVENT_POOL = {
    "medical_bill": Event(
        "Medical Bill",
        "Unexpected medical expenses hit you hard.",
        medical_bill_effect
    ),
    "investment_loss": Event(
        "Investment Loss",
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
    ),
    # Strategic Events
    "emergency_fund": Event(
        "Emergency Fund Check",
        "An unexpected opportunity or crisis tests your preparedness.",
        emergency_fund_bonus_effect
    ),
    "upgrade_synergy": Event(
        "Equipment Maintenance Crisis",
        "Multiple upgrades create unexpected maintenance burdens.",
        upgrade_maintenance_crisis_effect,
        requires_upgrades=True
    ),
    "savings_milestone": Event(
        "Economic Crisis",
        "Market volatility and inflation affect your savings.",
        savings_devaluation_crisis_effect
    ),
    "equipment_warning": Event(
        "Equipment Assessment",
        "Time to evaluate your farming equipment condition.",
        equipment_warning_effect,
        requires_upgrades=True
    ),
    "workforce_efficiency": Event(
        "Labor Relations Crisis",
        "Workforce issues disrupt farm operations.",
        labor_dispute_crisis_effect,
        requires_upgrades=True
    ),
    "market_demand": Event(
        "Market Demand Shift",
        "Consumer preferences change, affecting farm products.",
        market_demand_shift_effect,
        requires_upgrades=True
    ),
    "diversification": Event(
        "Income Diversification",
        "Your various income sources are evaluated for stability.",
        diversification_bonus_effect,
        requires_upgrades=True
    )
}


#Event Chances of happening
#Higher percentages mean higher chance of that event happening
EVENT_PERCENTAGES = {
    "medical_bill": 0.10,
    "investment_loss": 0.08,
    "tax_increase": 0.09,
    "stock_boom": 0.04,
    "business_bonus": 0.045,
    # Strategic events
    "emergency_fund": 0.09,
    "upgrade_synergy": 0.07,
    "savings_milestone": 0.065,
    "equipment_warning": 0.06,
    "workforce_efficiency": 0.05,
    "market_demand": 0.035,
    "diversification": 0.015
}


def get_random_event(): 

   # Randomly select one event from EVENT_POOL based on EVENT_PERCENTAGES.
    # Returns the selected Event object, or None for no event (70% chance).

    # 50% chance of no event occurring
    if random.random() < 0.50:
        return None

    names = list(EVENT_PERCENTAGES.keys())       # Event identifiers
    percentages = list(EVENT_PERCENTAGES.values())   # Corresponding probabilities
    selected = random.choices(names, weights=percentages, k=1)[0]  # Pick one key
    return EVENT_POOL[selected]              # Return the matching Event object


def trigger_event(player, game_upgrades=None):

    # Selects and applies a random event to the player.
    # Returns a dictionary summarizing the event and its result text, or None if no event occurs.

    event = get_random_event()               # Pick a random event
    if event is None:
        return None  # No event occurred

    result_text = event.apply(player, game_upgrades)        # Apply the event’s effect
    return {
        "event_name": event.name,
        "description": event.description,
        "result": result_text
    }

if __name__ == "__main__":
    print("\nSorry, but events.py can only be imported!")
