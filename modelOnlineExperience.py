from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from agentOnlineExperience import CustomerOnlineExperienceAgent

class OnlineExperienceModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            agent = CustomerOnlineExperienceAgent(i, self)
            self.schedule.add(agent)

        self.datacollector = DataCollector(agent_reporters={"Experience with Online Services": "experience_with_online_services", "Ethnicity": "ethnic"})        
        #indent maybe? i will see

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        # Manually round the step values in the collected data
        self.datacollector.get_agent_vars_dataframe().reset_index()['Step'] = \
            self.datacollector.get_agent_vars_dataframe().reset_index()['Step'].round(0).astype(int)

    def update(self, val):
        # Ensure the step count is an integer
        step_count = 10

        # Create dictionaries to store experience with online services data for each ethnic group
        experience_with_online_services_data = {"Black": [], "White": [], "Asian": []}

        # Clear Agents
        for agent in self.schedule.agents:
            agent.get_initial_experience()
            agent.step_count = 0
            agent.last_social_support = 0

        # Iterate over the selected social support values in 20 steps
        for step in range(step_count):
            # Adjust social support based on the slider value
            social_support = val 

            # Set social support for each agent in the model. Selected social_support value is increased in equal step_count interval
            for agent in self.schedule.agents:
              # agent.social_support_change = (social_support - agent.social_support) * step / step_count * 1.0 #equally divided for each step
              # agent.social_support_change = max(-1, min(1, agent.social_support_change))
              # THE ONE ABOVE IS CUMULATIVE, THE ONE BELOW IS BASED ON PERCENTAGE   
                agent.social_support= social_support * step / step_count * 1.0  #equally divided for each step
                agent.social_support= max(-1, min(1, agent.social_support_change))
                agent.step()

            self.step()

            # Collect Experience with Online Services data for each ethnic group for the current step
            agent_data = self.datacollector.get_agent_vars_dataframe().reset_index()
            for ethnic_group in experience_with_online_services_data.keys():
                group_data = agent_data[agent_data['Ethnicity'] == ethnic_group]
                avg_experience_with_online_services = group_data['Experience with Online Services'].mean()
                experience_with_online_services_data[ethnic_group].append(avg_experience_with_online_services)

        # Clear previous plot
        ax.clear()

        # Plot Experience with Online Services values for each ethnic group over 20 steps
        for ethnic_group, values in experience_with_online_services_data.items():
            ax.plot(range(1, step_count + 1), values, marker='o', label=f'{ethnic_group} Group')

        # Set labels and title
        ax.set_xlabel("Step")
        ax.set_ylabel("Average Experience with Online Services")
        ax.set_title("Experience with Online Services Levels Over 20 Steps by Ethnicity")

        # Set the major ticks on the x-axis with intervals of 1
        ax.set_xticks(range(1, step_count + 1))

        # Set initial y-axis limits between -1 and 1
        ax.set_ylim(-1, 1)

        # Show updated plot
        ax.legend(loc="upper left")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.draw()  # Use plt.draw() instead of plt.show() for interactive updating

    def reset_agents(self, event):
        # Create a new instance of RandomActivation
        new_schedule = RandomActivation(self)

        # Add new agents to the schedule
        for i in range(self.num_agents):
            agent = CustomerOnlineExperienceAgent(i, self)
            new_schedule.add(agent)

        # Replace the existing schedule with the new one
        self.schedule = new_schedule

        # Clear data collector
        self.datacollector = DataCollector(agent_reporters={"Experience with Online Services": "experience_with_online_services", "Ethnicity": "ethnic"})

        # Clear previous plot
        ax.clear()

        # Plot average Experience with Online Services over time for each ethnic group with error bars
        ethnic_data = self.datacollector.get_agent_vars_dataframe().reset_index()
        experience_with_online_services_data = ethnic_data.groupby(['Step', 'Ethnicity'])['Experience with Online Services'].mean().reset_index()

        for ethnic_group in experience_with_online_services_data['Ethnicity'].unique():
            group_data = experience_with_online_services_data[experience_with_online_services_data['Ethnicity'] == ethnic_group]

            if not group_data.empty:
                # Round the step values to integers for the plot
                x_values = group_data['Step'].round(0).astype(int)
                ax.errorbar(x_values, group_data['Experience with Online Services'],
                            yerr=group_data.groupby('Step')['Experience with Online Services'].std(),
                            label=f'{ethnic_group} Group', linewidth=2, marker='o')
            else:
                print(f"No data for {ethnic_group} Group")

        # Set labels and title
        ax.set_xlabel("Step")
        ax.set_ylabel("Average Experience with Online Services")
        ax.set_title("Average Experience with Online Services Levels Over Time by Ethnicity")

        # Add slider for social support
        axcolor = 'lightgoldenrodyellow'
        ax_social_support = plt.axes([0.3, 0.93, 0.4, 0.03], facecolor=axcolor)  # Adjusted position and size
        social_support_slider = Slider(ax_social_support, 'Social Support', 0, 1, valinit=0.0, valstep=0.01)  # Set valinit to 0.0

        # Attach the sliders to the update function
        social_support_slider.on_changed(self.update) #why do we have this for the second time

        social_support_slider.label.set_text("")

        # Create reset button
        reset_button = self.create_reset_button()

        # Set legend and adjust layout
        ax.legend(loc="upper left")
        plt.grid(True, linestyle='--', alpha=0.7)

        # Set initial y-axis limits between -1 and 1
        ax.set_ylim(-1, 1)

        # Show the updated plot
        plt.draw()

    def create_reset_button(self):
        # Create a button to reset agents
        ax_reset_button = plt.axes([0.8, 0.01, 0.1, 0.04])  # Adjusted position and size
        reset_button = Button(ax_reset_button, 'Reset', color='lightgoldenrodyellow')
        reset_button.on_clicked(self.reset_agents)
        return reset_button

    def plot_agents_first_step(self):
        # Create subplots for each agent
        fig, axs = plt.subplots(5, 6, figsize=(15, 12))  # Assuming there are 26 agents, adjust rows and columns as needed

        for i, agent in enumerate(self.schedule.agents):
            row = i // 6
            col = i % 6

            # Plot experience for the first step
            axs[row, col].plot([1], [agent.experience_with_online_services], marker='o', label=f'Agent {agent.unique_id}')
            axs[row, col].set_title(f'Agent {agent.unique_id}')
            axs[row, col].set_xlabel("Step")
            axs[row, col].set_ylabel("Experience with Online Services")
            axs[row, col].legend()

        plt.tight_layout()
        plt.show()


# Initial values
width = 10
height = 10

# Create initial model
model = OnlineExperienceModel(26, width, height)  # Set the initial number of agents to 26

# Plot every agent for the first step
model.plot_agents_first_step()

# Use Seaborn for improved styles
import seaborn as sns
sns.set(style="whitegrid")

# Create a figure with subplots
fig, ax = plt.subplots(figsize=(12, 8))

# Plot average Experience with Online Services over time for each ethnic group with error bars
ethnic_data = model.datacollector.get_agent_vars_dataframe().reset_index()
experience_with_online_services_data = ethnic_data.groupby(['Step', 'Ethnicity'])['Experience with Online Services'].mean().reset_index()
for ethnic_group in experience_with_online_services_data['Ethnicity'].unique():
    group_data = experience_with_online_services_data[experience_with_online_services_data['Ethnicity'] == ethnic_group]

    if not group_data.empty:
        # Round the step values to integers for the plot
        x_values = group_data['Step'].round(0).astype(int)
        ax.errorbar(x_values, group_data['Experience with Online Services'],
                    yerr=group_data.groupby('Step')['Experience with Online Services'].std(),
                    label=f'{ethnic_group} Group', linewidth=2, marker='o')
    else:
        print(f"No data for {ethnic_group} Group")

# Set labels and title
ax.set_xlabel("Step")
ax.set_ylabel("Average Experience with Online Services")
ax.set_title("Average Experience with Online Services Levels Over Time by Ethnicity")

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

# Set initial y-axis limits between -1 and 1
ax.set_ylim(-1, 1)

# Show the updated plot
plt.show()