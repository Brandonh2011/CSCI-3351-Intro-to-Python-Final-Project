from player import Player

class TurnSystem:
    def __init__(self):
        self.player = Player()
    
    def oneTurn(self):
        #applies interests to savings
        interested_earned = self.player.bank.applyInterest()
        
        #200 per turn before upgrades
        base_income = 200
        self.player.addMoney(base_income)
        
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
            "income" : base_income,
            "interestEarned" : interested_earned,
            "checking" : self.player.getMoney(),
            "savings" : self.player.bank.getSavings(),
            "networth" :  self.player.getMoney() + self.player.bank.getSavings(),
            "happiness" : self.player.getHappiness()
        }
        
         #moving money to savings
    def deposit_to_savings(self, amount):
            return self.player.bank(amount, self.player)
        
        #moving money to checking
    def withdraw_from_savings(self, amount):
        return self.player.bank.withdraw(amount, self.player)
    

if __name__ == "__main__":
    print("\nSorry, but turn.py can only be imported!")