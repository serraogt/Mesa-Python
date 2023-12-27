
from mesa import Agent
import random

class CustomerOnlineExperienceAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        #self.age = self.random.randint(18, 80) not used yet
        self.ethnic = self.get_ethnicity() #dene
        self.step_count = 0
        self.social_support = 0 #self.get_social_support()
        self.social_support_change = 0
        self.experience_with_online_services =  self.get_initial_experience() # or Initialize as neutral
        # it is something to decide
#
        
    def get_initial_experience(self):
        if self.ethnic == "White":
            return random.choice([1, 0, -1, 1, 1, 0]) * 1.0  # Choose from 1 or 0 for more positive values
        elif self.ethnic == "Asian":
            return random.choice([-1, 0, 1, 0]) * 1.0 # Choose from -1, 0, or 1 for a balanced range
        else:
            return random.choice([0, -1, 0, -1, -1, 1]) * 1.0 # Choose from 0 or 1 for more positive values

    def get_social_support(self):
        # Set social support based on ethnicity
        if self.ethnic == "White":
            return self.random.uniform(0.0, 0.1)
        elif self.ethnic == "Asian":
            return self.random.uniform(0.1, 0.2)
        else:
            return self.random.uniform(0.2, 0.3)

    def set_social_support(self, i): 
        self.social_support=i

    def get_ethnicity(self):
        # Assign ethnic based on probabilities
        rand_num = random.uniform(0, 1)
        if rand_num < 0.3:
            return "Asian"
        elif rand_num < 0.6:
            return "Black"
        else:
            return "White"

    def step(self):
        self.step_count += 1

        # change online experience according to social support change
        if self.ethnic == "White":
            self.experience_with_online_services = self.get_initial_experience() + ( 0.1 * ((self.social_support)*1.0))
        elif self.ethnic == "Asian":
            self.experience_with_online_services = self.get_initial_experience() + ( 0.2 * ((self.social_support)*1.0))
        else:
            self.experience_with_online_services = self.get_initial_experience() + ( 0.3 * ((self.social_support)*1.0))

        # Ensure the experience is within the valid range
        self.experience_with_online_services = max(-1, min(1, self.experience_with_online_services))

        # Print statements for debugging
        
        print(f"Agent {self.unique_id}")
        print(f"Step Count: {self.step_count}")
        print(f"Ethnicity: {self.ethnic}")
        print(f"Online Experience: {self.experience_with_online_services}")
        print(f"Social Support: {self.social_support}")
        print(f"Social Support Change: {self.social_support_change}")
        print("------")