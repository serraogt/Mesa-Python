from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from agentNew import CustomerNewAgent
import random

class DiscriminationModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            agent = CustomerNewAgent(i, self)
            self.schedule.add(agent)

        self.datacollector = DataCollector(agent_reporters={"Discrimination": "discriminated", "Ethnicity": "ethnic"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        # Manually round the step values in the collected data
        self.datacollector.get_agent_vars_dataframe().reset_index()['Step'] = \
            self.datacollector.get_agent_vars_dataframe().reset_index()['Step'].round(0).astype(int)

    def update(self, val):
        # Ensure the step count is an integer
        step_count = 20

        # Create dictionaries to store discrimination data for each ethnic group
        discrimination_data = {"Black": [], "White": [], "Asian": []}

        # Clear Agents
        for agent in self.schedule.agents:
            agent.discriminated = 0.9
            agent.step_count = 0
            agent.last_social_support = agent.get_social_support()

        # Iterate over the selected social support values in 20 steps
        for step in range(step_count):
            
            # Adjust social support based on the slider value
            social_support = val

            # Set social support for each agent in the model
            for agent in self.schedule.agents:

                if agent.social_support < social_support:
                    agent.last_social_support = agent.social_support + social_support * (step_count - step) / step_count
                else:
                    agent.last_social_support = agent.social_support - social_support * (step_count - step) / step_count
    
                agent.step()
                
            self.step()

            # Collect discrimination data for each ethnic group for the current step
            agent_data = self.datacollector.get_agent_vars_dataframe().reset_index()
            for ethnic_group in discrimination_data.keys():
                group_data = agent_data[agent_data['Ethnicity'] == ethnic_group]
                avg_discrimination = group_data['Discrimination'].mean()
                discrimination_data[ethnic_group].append(avg_discrimination)

        # Clear previous plot
        ax.clear()

        # Plot discrimination values for each ethnic group over 20 steps
        for ethnic_group, values in discrimination_data.items():
            ax.plot(range(1, step_count + 1), values, marker='o', label=f'{ethnic_group} Group')

        # Set labels and title
        ax.set_xlabel("Step")
        ax.set_ylabel("Average Discrimination")
        ax.set_title("Discrimination Levels Over 20 Steps by Ethnicity")

        # Set the major ticks on the x-axis with intervals of 1
        ax.set_xticks(range(1, step_count + 1))

        # Show updated plot
        ax.legend(loc="upper left")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.draw()  # Use plt.draw() instead of plt.show() for interactive updating

    def reset_agents(self, event):
        # Create a new instance of RandomActivation
        new_schedule = RandomActivation(self)

        # Add new agents to the schedule
        for i in range(self.num_agents):
            agent = CustomerNewAgent(i, self)
            new_schedule.add(agent)

        # Replace the existing schedule with the new one
        self.schedule = new_schedule

        # Clear data collector
        self.datacollector = DataCollector(agent_reporters={"Discrimination": "discriminated", "Ethnicity": "ethnic"})

        # Clear previous plot
        ax.clear()

        # Plot average discrimination over time for each ethnic group with error bars
        ethnic_data = self.datacollector.get_agent_vars_dataframe().reset_index()
        discrimination_data = ethnic_data.groupby(['Step', 'Ethnicity'])['Discrimination'].mean().reset_index()

        for ethnic_group in discrimination_data['Ethnicity'].unique():
            group_data = discrimination_data[discrimination_data['Ethnicity'] == ethnic_group]

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

        # Add slider for social support
        axcolor = 'lightgoldenrodyellow'
        ax_social_support = plt.axes([0.3, 0.93, 0.4, 0.03], facecolor=axcolor)  # Adjusted position and size
        social_support_slider = Slider(ax_social_support, 'Social Support', 0, 1, valinit=0.0, valstep=0.01)  # Set valinit to 0.0

        # Attach the sliders to the update function
        social_support_slider.on_changed(model.update)

        social_support_slider.label.set_text("")

        # Create reset button
        reset_button = self.create_reset_button()

        # Set legend and adjust layout
        ax.legend(loc="upper left")
        plt.grid(True, linestyle='--', alpha=0.7)

        # Show the updated plot
        plt.draw()

    def create_reset_button(self):
        # Create a button to reset agents
        ax_reset_button = plt.axes([0.8, 0.01, 0.1, 0.04])  # Adjusted position and size
        reset_button = Button(ax_reset_button, 'Reset', color='lightgoldenrodyellow')
        reset_button.on_clicked(self.reset_agents)
        return reset_button

# Initial values
width = 10
height = 10

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

# Add slider for social support
axcolor = 'lightgoldenrodyellow'
ax_social_support = plt.axes([0.3, 0.93, 0.4, 0.03], facecolor=axcolor)  # Adjusted position and size
social_support_slider = Slider(ax_social_support, 'Social Support', 0, 1, valinit=0.0, valstep=0.01)  # Set valinit to 0.0

# Attach the sliders to the update function
social_support_slider.on_changed(model.update)

# Create reset button
reset_button = model.create_reset_button()

# Set legend and adjust layout
ax.legend(loc="upper left")
plt.grid(True, linestyle='--', alpha=0.7)

# Show the updated plot
plt.show()
