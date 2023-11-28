from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import CustomerAgent
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

class DiscriminationModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            agent = CustomerAgent(i, self)
            self.schedule.add(agent)

        self.datacollector = DataCollector(agent_reporters={"Discrimination": "discriminated", "BuyCount": "buy_count", "Ethnicity": "ethnic"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        # Manually round the step values in the collected data
        self.datacollector.get_agent_vars_dataframe().reset_index()['Step'] = \
            self.datacollector.get_agent_vars_dataframe().reset_index()['Step'].round(0).astype(int)

def update(val):
    # Ensure the step count is an integer
    step_count = round(step_slider.val)

    # Set the number of agents to a predefined value (e.g., 6)
    num_agents = 6

    model = DiscriminationModel(num_agents, width, height)

    for i in range(step_count):
        model.step()

    agent_data = model.datacollector.get_agent_vars_dataframe().reset_index()

    # Clear previous plot
    ax.clear()

    # Plot average discrimination over time for each ethnic group with error bars
    ethnic_data = agent_data.groupby(['Step', 'Ethnicity'])['Discrimination'].mean().reset_index()
    for ethnic_group in ethnic_data['Ethnicity'].unique():
        group_data = ethnic_data[ethnic_data['Ethnicity'] == ethnic_group]

        if not group_data.empty:
            # Manually cast the step values to integers for the plot
            ax.errorbar(group_data['Step'].astype(int), group_data['Discrimination'],
                        yerr=group_data.groupby('Step')['Discrimination'].std(),
                        label=f'{ethnic_group} Group', linewidth=2, marker='o')
        else:
            print(f"No data for {ethnic_group} Group")

    # Set labels and title
    ax.set_xlabel("Step")
    ax.set_ylabel("Average Discrimination")
    ax.set_title("Average Discrimination Levels Over Time by Ethnicity")

    # Ensure the x-axis limits cover the entire range of your data
    ax.set_xlim(0.5, step_count + 0.5)

    # Set the major ticks on the x-axis with intervals of 1
    ax.set_xticks(range(1, step_count + 1))
    ax.set_xticklabels(range(1, step_count + 1))

    # Show updated plot
    ax.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

# Initial values
width = 10
height = 10
last = 10

# Create initial model
model = DiscriminationModel(6, width, height)  # Set the initial number of agents to 6

# Initial collected data
agent_data = model.datacollector.get_agent_vars_dataframe().reset_index()

# Use Seaborn for improved styles
import seaborn as sns
sns.set(style="whitegrid")

# Create a figure with subplots
fig, ax = plt.subplots(figsize=(12, 8))

# Plot average discrimination over time for each ethnic group with error bars
ethnic_data = agent_data.groupby(['Step', 'Ethnicity'])['Discrimination'].mean().reset_index()
for ethnic_group in ethnic_data['Ethnicity'].unique():
    group_data = ethnic_data[ethnic_data['Ethnicity'] == ethnic_group]

    if not group_data.empty:
        # Round the step values to integers for the plot
        x_values = group_data['Step'].round(0).astype(int)
        ax.errorbar(x_values, group_data['Discrimination'],
                    yerr=group_data.groupby('Step')['Discrimination'].std(),
                    label=f'{ethnic_group} Group', linewidth=2, marker='o')
    else:
        print(f"No data for {ethnic_group} Group")

# Set labels and title
ax.set_xlabel("Step")
ax.set_ylabel("Average Discrimination")
ax.set_title("Average Discrimination Levels Over Time by Ethnicity")

# Add slider for the step count
axcolor = 'lightgoldenrodyellow'
ax_step = plt.axes([0.1, 0.93, 0.65, 0.03], facecolor=axcolor)
step_slider = Slider(ax_step, 'Step Count', 1, 20, valinit=1, valstep=1)

# Attach the sliders to the update function
step_slider.on_changed(update)

# Set legend and adjust layout
ax.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# Show the plot
plt.show()
