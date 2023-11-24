from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import CustomerAgent
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import pandas as pd

class DiscriminationModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            agent = CustomerAgent(i, self)
            self.schedule.add(agent)

        self.datacollector = DataCollector(agent_reporters={"Happiness": "happiness", "BuyCount": "buy_count"})
    
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()    


width = 10
height = 10
num_agents = 6
model = DiscriminationModel(num_agents, width, height)

last = 10  # Increase the number of steps for a longer simulation
for i in range(last):
    model.step()

# Collected data
agent_data = model.datacollector.get_agent_vars_dataframe().reset_index()

# Use Seaborn for improved styles
import seaborn as sns
sns.set(style="whitegrid")

# Create a figure with subplots
fig, ax = plt.subplots(figsize=(12, 8))

# Plot happiness over time for each agent with error bars
for agent_id in range(num_agents):
    agent_data_single = agent_data[agent_data["AgentID"] == agent_id]
    ax.errorbar(agent_data_single["Step"], agent_data_single["Happiness"],
                yerr=agent_data_single.groupby("Step")["Happiness"].std(),
                label=f'Agent {agent_id}', linewidth=2, marker='o')

# Set labels and title
ax.set_xlabel("Step")
ax.set_ylabel("Happiness")
ax.set_title("Agent Happiness Levels Over Time")

# Set legend and adjust layout
ax.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# Show plot
plt.show()
