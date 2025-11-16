
from bank import Bank

class Player:
    def __init__(self, name):
        self.__name = name #potential player name input
        self.__money = 200 #starting cash
        self.__happiness = 100 #starts fully happy
        self.__debt = 0 #
        self.__current_year = 0 #turn
        self.bank = Bank()

    def debtInterest(self):
        #punishment if in debt
        if self.__money < 0:
            self.__money *= 1.05 #5% interest
            
    #Getters
    def getName(self):
        return self.__name
    
    def getMoney(self):
        return self.__money
    
    def getHappiness(self):
        return self.__happiness
    
    def getDebt(self):
        return self.__debt
    
    def getYear(self):
        return self.__current_year 
    
    #Checkers
    def canAfford(self, cost):
        #Checks if player has enough money
        return self.__money >= cost
    
    def isBankrupt(self):
        #if player gets a game over
        return self.__money < -500
    
    #Setters
    def addMoney(self, amount):
        self.__money += amount
        self.debtInterest()
        
    def minusMoney(self, amount):
        self.__money -= amount
        self.debtInterest()
        
    def addHappiness(self, amount):
        self.__happiness += amount
    
    def minusHappiness(self, amount):
        self.__happiness-= amount
    
    def nextYear(self):
        self.__current_year += 1
    
    
if __name__ == "__main__":
    print("\nSorry, but player.py can only be imported!")