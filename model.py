from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import HappinessAgent
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import pandas as pd

class HappinessModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            agent = HappinessAgent(i, self)
            #x = random.randrange(self.grid.width)
            #y = random.randrange(self.grid.height)
            #self.grid.place_agent(agent, (x, y))
            #I commented those out since there will be no plane
            self.schedule.add(agent)

        self.datacollector = DataCollector(agent_reporters={"Happiness": "happiness","BuyCount": "buy_count"})
    
   
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()    


width = 10
height = 10
num_agents = 6
model = HappinessModel(num_agents, width, height)

last = 4
for i in range(last):  # after 4 calls
    model.step()

# collected data
agent_data = model.datacollector.get_agent_vars_dataframe().reset_index()

for i in range(len(agent_data)):
    agent_id = agent_data.loc[i, "AgentID"]
    buy_count = agent_data.loc[i, "BuyCount"]  


initial_data = agent_data[agent_data["Step"] == 0]
updated_data = agent_data[agent_data["Step"] == last-1]

# the graph of the change in happiness
plt.scatter(initial_data["AgentID"], initial_data["Happiness"], label='Initial Happiness', c='lightblue')
plt.scatter(updated_data["AgentID"], updated_data["Happiness"], label='Updated Happiness after4 calls', c='darkblue')
plt.xlabel("Agent")
plt.ylabel("Happiness")
plt.title("Agent Happiness Levels")
plt.ylim(0, 1) 
plt.legend()
plt.show()
