class Upgrade:
    def __init__(self):
        self.upgrades = {
            #Tier 1 Upgrades
            "land_increase_1":{
                "name": "Land Expansion",
                "cost": 300,
                "description": "Increase your land holdings to generate more income.",
                "tier": 1,
                "max_level": 1,
                "current_level": 0
            },
            "hand_tools":{
                "name": "Hand Tools",
                "cost": 200,
                "description": "Basic tools to improve efficiency.",
                "tier": 1,
                "max_level": 3,
                "current_level": 0
            },
            "Employee":{
                "name": "Hire Employee",
                "cost": 400,
                "description": "Hire an employee to help with your business.",
                "tier": 1,
                "max_level": 2,
                "current_level": 0
            },
            #Tier 2 Upgrades
            "land_increase_2":{
                "name": "Land Expansion",
                "cost": 800,
                "description": "Further increase your land to boost income.",
                "tier": 2,
                "max_level": 1,
                "current_level": 0
            },
            "potato_crops":{
                "name": "Potato Crops",
                "cost":250,
                "description": "Unlock potatoes: $30 income every other turn.",
                "tier": 2,
                "max_level": 1,
                "current_level": 0
            },
            
            "Machinery":{
                "name": "Buy Machinery",
                "cost": 1000,
                "description": "Invest in machinery to significantly boost productivity.",
                "tier": 2,
                "max_level": 2,
                "current_level": 0
            },
            
            "farmers_market_stall":{
                "name": "Farmers Market Stall",
                "cost": 600,
                "description": "Set up a stall at the farmers market to increase sales.",
                "tier": 2,
                "max_level": 1,
                "current_level": 0
            },
            "fertilizerConsumable":{
                "name": "Fertilizer",
                "cost": 150,
                "description": "Boost crop yeild next turn by 50%",
                "tier": 2,
            },
            #Tier 3 Upgrades
            "chicken":{
                "name": "Chicken Coop",
                "cost": 2000,
                "description": "Raise chickens to diversify your farm income.",
                "tier": 3,
                "max_level": 1,
                "current_level": 0
            }
        }
        self.__num_workers = 0
        self.__fertilizer_active = False
        self.__fertilizer_queue = False
        
    def canPurchase(self, upgrade_key, player):
        #Checks if player can afford upgrade and if not maxed out
        upgrade = self.upgrades[upgrade_key]
        return player.canAfford(upgrade["cost"]) and upgrade["current_level"] < upgrade["max_level"]
    
    def purchaseUpgrade(self, upgrade_key, player):
        #Buys an upgrade if possible
        if upgrade_key not in self.upgrades:
            return "Invalid upgrade selection."
        
        upgrade = self.upgrades[upgrade_key]
        
         #Calculates cost based on current level
        cost = upgrade["cost"] * (upgrade["current_level"] + 1)
        
        #Checks if purchase is valid or not
        if not self.canPurchase(upgrade_key, player):
            if upgrade["current_level"] >= upgrade["max_level"]:
                return False, f"{upgrade['name']} already maxed out"
            else:
                return False, f"Can't afford {upgrade['name']}"
            
        #if a worker is bought
        if upgrade_key == "Employee":
            player.minusMoney(cost)
            self.__num_workers += 1
            player.addHappiness(2)
            upgrade["current_level"] += 1
            return True, f"Hired worker #{self.__num_worker}"
           
        elif upgrade_key == "fertilizerConsumable":
            player.minusMoney(cost)
            #To ensure its active for next turn
            self.__fertilizer_queue = True
            player.addHappiness(1)
            
        else:
            player.minusMoney(cost)
            upgrade["current_level"] += 1
            player.addHappiness(2)
            return True, f"Purchased {upgrade['name']}"
    

    #Total income based on all ugprades
    def calculateIncome(self):
        #200 per turn before ugprades
        base_income = 200
        
        #Land Multipliers
        land_mult = 1.0
        
        if self.upgrades['land_increase_1']["current_level"]> 0:
            land_mult *= 1.3 #30% boost
        if self.upgrades['land_increase_2']["current_level"]> 0:
            land_mult *= 1.4 #40% boost
            
        #Hand tools multiplier
        tools_mult = 1.0
        if self.upgrades["hand_tools"]["current_level"] > 0:
            #10 percent increase per level
            tools_mult *= (1.1 ** self.upgrades["hand_tools"]["current_level"]) 
        
        #Machinery Tool Multiplier
        machinery_mult = 1.0
        if self.upgrades["Machinery"]["current_level"] > 0:
            machinery_mult *= (1.1 ** self.upgrades["Machinery"]["current_level"])
        
        #Worker multiplier
        worker_mult = 1.0 + (self.__num_workers * 0.3)
        
        fertilizer_boost = 0
        #Fertilizer boost if active
        if self.__fertliizer_active:
            fertilizer_boost = 1.5
            
        
        #Chicken passive income
        chicken_income = 0    
        if self.upgrades["chicken"]["current_level"] > 0:
            chicken_income = 450 
        
        #potato income
        potato_income = 0    
        if self.upgrades["potato_crops"]["current_level"] > 0:
            potato_income = 250 
            
        #market multiplier
        market_mult = 1.0
        
        if self.upgrades["farmers_market_stall"]["current_level"] > 0:
            market_mult *= 1.5
        
        total = (base_income * land_mult * tools_mult * market_mult * machinery_mult + chicken_income + potato_income) * fertilizer_boost * worker_mult
    
        return total

    #Fertilizer helper functions
    def isFertilizerActive(self):
        return self.__fertilizer_active
    def isFerterlizerQueued(self):
        return self.__fertilizer_queue
    def setFertilizerActive(self, active):
        self.__fertilizer_active = active
    def setFertilizerQueue(self, queue):
        self.__fertilizer_queue = queue