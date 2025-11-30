from player import Player
from upgrades import Upgrade

class TurnSystem:
    def __init__(self):
        self.player = Player("Player1")
        self.upgrades = Upgrade()
    
    def oneTurn(self):
        self.upgrades.setFertilizerActive(self.upgrades.isFerterlizerQueued())
        #Resets fertilizer
        self.upgrades.setFertilizerQueue(False)
        
        #applies interests to savings
        interested_earned = self.player.bank.applyInterest()
        
        #200 per turn before upgrades
        income = self.upgrades.calculateIncome()
        self.player.addMoney(income)
        
        #Gameover results
        if self.player.isBankrupt():
            return {
                "status": "Bankrupt",
                "year" : self.player.getYear(),
                "checking" : self.player.getMoney(), 
                "savings" : self.player.bank.getSavings(),
                "networth" : self.player.getMoney() + self.player.bank.getSavings()
            }
        
        #advances year count
        self.player.nextYear()
        
        #turn summary
        return {
            "year" : self.player.getYear(),
            "income" : income,
            "interestEarned" : interested_earned,
            "checking" : self.player.getMoney(),
            "savings" : self.player.bank.getSavings(),
            "networth" :  self.player.getMoney() + self.player.bank.getSavings(),
            "happiness" : self.player.getHappiness()
        }
        
         #moving money to savings
    def deposit_to_savings(self, amount):
            return self.player.bank.deposit(amount, self.player)
        
        #moving money to checking
    def withdraw_from_savings(self, amount):
        return self.player.bank.withdraw(amount, self.player)
    

if __name__ == "__main__":
    print("\nSorry, but turn.py can only be imported!")