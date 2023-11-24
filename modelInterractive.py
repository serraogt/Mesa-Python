from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import CustomerAgent
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Slider, Button

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


def update(val):
    num_agents = int(num_agents_slider.val)
    model = DiscriminationModel(num_agents, width, height)

    for i in range(last):
        model.step()

    # Collected data
    agent_data = model.datacollector.get_agent_vars_dataframe().reset_index()

    # Clear previous plot
    ax.clear()

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

    # Show updated plot
    plt.show()


# Initial values
width = 10
height = 10
num_agents = 6
last = 10

# Create initial model
model = DiscriminationModel(num_agents, width, height)

# Initial collected data
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

# Add slider for number of agents
axcolor = 'lightgoldenrodyellow'
ax_num_agents = plt.axes([0.1, 0.01, 0.65, 0.03], facecolor=axcolor)
num_agents_slider = Slider(ax_num_agents, 'Num Agents', 1, 20, valinit=num_agents, valstep=1)

# Add button to update the plot
ax_button = plt.axes([0.8, 0.01, 0.1, 0.03])
button = Button(ax_button, 'Update', color=axcolor, hovercolor='0.975')


# Define the update function for the button
def update_button(val):
    update(val)


# Attach the update function to the button
button.on_clicked(update_button)

# Attach the slider to the update function
num_agents_slider.on_changed(update)

# Show the plot
plt.show()
