from mesa import Agent
import random

class CustomerAgent(Agent):
    """an agent with initial happiness"""

    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)
        self.age=self.random.randint(18, 80)
        self.happiness = self.getHappiness()
        self.discriminated = 0.1
        self.ethnic = self.get_ethnicity()
        self.buy_count = 0 

    def getBuyCount(self):
        buy_count=buy_count
        return buy_count
    
    def get_ethnicity(self):
        # Assign ethnic based on probabilities
        rand_num = random.uniform(0, 1)
        if rand_num < 0.3:
            return "Asian"
        elif rand_num < 0.6:
            return "Mixed"
        else:
            return "White"
    
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

        rand_num = random.uniform(0, 1)
        if  self.ethnic == "White":
            if self.discriminated<1 and rand_num<0.1:
                self.discriminated += 0.01
        elif  self.ethnic == "Asian":
            if self.discriminated<1 and rand_num <0.5:
                self.discriminated += 0.12
        else:
            if self.discriminated<1 and rand_num<0.8:
                self.discriminated += 0.13
        
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
  
