from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import CustomerAgent
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

class DiscriminationModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            agent = CustomerAgent(i, self)
            self.schedule.add(agent)

        self.datacollector = DataCollector(agent_reporters={"Happiness": "happiness", "BuyCount": "buy_count", "Ethnicity": "ethnic"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

def update(val):
    num_agents = int(num_agents_slider.val)
    model = DiscriminationModel(num_agents, width, height)

    for i in range(last):
        model.step()

    agent_data = model.datacollector.get_agent_vars_dataframe().reset_index()

    # Updated: Retrieve the unique step values and reset them starting from 1
    step_values = agent_data['Step'].unique()
    agent_data['Step'] = agent_data['Step'].replace(dict(zip(step_values, range(1, len(step_values) + 1))))

    # Clear previous plot
    ax.clear()

    # Plot average happiness over time for each ethnic group with error bars
    ethnic_data = agent_data.groupby(['Step', 'Ethnicity'])['Happiness'].mean().reset_index()
    for ethnic_group in ethnic_data['Ethnicity'].unique():
        group_data = ethnic_data[ethnic_data['Ethnicity'] == ethnic_group]
        ax.errorbar(group_data['Step'], group_data['Happiness'],
                    yerr=group_data.groupby('Step')['Happiness'].std(),
                    label=f'{ethnic_group} Group', linewidth=2, marker='o')

    # Set labels and title
    ax.set_xlabel("Step")
    ax.set_ylabel("Average Happiness")
    ax.set_title("Average Happiness Levels Over Time by Ethnicity")

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

# Plot average happiness over time for each ethnic group with error bars
ethnic_data = agent_data.groupby(['Step', 'Ethnicity'])['Happiness'].mean().reset_index()
for ethnic_group in ethnic_data['Ethnicity'].unique():
    group_data = ethnic_data[ethnic_data['Ethnicity'] == ethnic_group]
    ax.errorbar(group_data['Step'], group_data['Happiness'],
                yerr=group_data.groupby('Step')['Happiness'].std(),
                label=f'{ethnic_group} Group', linewidth=2, marker='o')

# Set labels and title
ax.set_xlabel("Step")
ax.set_ylabel("Average Happiness")
ax.set_title("Average Happiness Levels Over Time by Ethnicity")

# Set legend and adjust layout
ax.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# Add slider for the number of agents
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
