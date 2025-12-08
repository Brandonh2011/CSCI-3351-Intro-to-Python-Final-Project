class Bank:
    def __init__(self):
        self.__savings = 0
        self.__interestRate = .10 #10% interest on savings
        
    def deposit(self, amount, player):
        if amount <= 0:
            return "Can't deposit a negative amount"
        
        if not player.canAfford(amount):
            return "Insufficient funds to deposit"
        else:
            player.minusMoney(amount) #removes from checking
            self.__savings += amount #adds to savings
            return "Money succesfully deposit"
        
    def withdraw(self, amount, player):
        if amount < 0:
            return "Can't withdraw a negative amount"
        elif amount > self.__savings:
            return "Not enough savings"
        else:
            self.__savings -= amount
            player.addMoney(amount)
            return "Money successfully withdrawn"
        
    def applyInterest(self):
        #adds interest to saving every turn
        interest = self.__savings * self.__interestRate
        self.__savings += interest
        return interest
    
    def getSavings(self):
        return self.__savings
    
if __name__ == "__main__":
    print("\nSorry, but bank.py can only be imported!")