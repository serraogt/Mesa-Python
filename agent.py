from mesa import Agent

class HappinessAgent(Agent):
    """an agent with initial happiness"""

    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)
        self.age=self.random.randint(18, 80)
        self.happiness = self.getHappiness()

    def getHappiness(self):
        baseHappiness=self.random.randint(3,7)/10
        #start with average happiness
        happiness= baseHappiness + ((50-self.age)/100)
        if (happiness>0.8):
            happiness=0.8
        elif (happiness<0.2):
            happiness=0.2    
        return happiness   

    def step(self) -> None: #returns none
        self.move()
       # if self.wealth > 0:
       # self.give_money()

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.happiness -= 1

    def move(self) -> None:
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)       
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
