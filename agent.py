from mesa import Agent
import random

class HappinessAgent(Agent):
    """an agent with initial happiness"""

    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)
        self.age=self.random.randint(18, 80)
        self.happiness = self.getHappiness()
        self.buy_count = 0 

    def getBuyCount(self):
        buy_count=buy_count
        return buy_count
    
    def getHappiness(self):
        baseHappiness=self.random.randint(3,7)/10
        #start with average happiness
        happiness= baseHappiness + ((50-self.age)/100)
        if (happiness>0.8):
            happiness=0.8
        elif (happiness<0.2):
            happiness=0.2    
            #slight normalisation
        return happiness   

    #def step(self) -> None: #returns none
     #   self.move()
       # if self.wealth > 0:
       # self.give_money()

    def step(self) -> None:
        if random.uniform(0,1) < self.happiness:
        #as happines increase, the chance they buy will increase
            self.buy_good()
        else: 
            self.refuse()

    
    
    def buy_good(self):
        if(self.happiness<0.9):
            self.happiness +=0.1
            self.buy_count += 1

    def refuse (self):
        if(self.happiness>0.1):
            self.happiness -=0.1
  
