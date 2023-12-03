# File: agentOnlineExperience.py

from mesa import Agent
import random

class CustomerOnlineExperienceAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.age = self.random.randint(18, 80)
        self.ethnic = self.get_ethnicity()
        self.step_count = 0
        self.social_support = 0.1
        self.last_social_support = self.get_social_support()
        self.experience_with_online_services = 0.9

    def get_social_support(self):
        # Set social support based on ethnicity
        if self.ethnic == "White":
            return self.random.uniform(0.0, 0.1)
        elif self.ethnic == "Asian":
            return self.random.uniform(0.1, 0.2)
        else:
            return self.random.uniform(0.2, 0.3)

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

        if self.ethnic == "White":
            if self.experience_with_online_services < 1 and self.experience_with_online_services > 0:
                # Decrease online experience with increasing social support for White
                self.experience_with_online_services -= 0.01 * (self.last_social_support - self.social_support)

        elif self.ethnic == "Asian":
            self.experience_with_online_services -= 0.02 * (self.last_social_support - self.social_support)

        else:
            if self.experience_with_online_services < 1 and self.experience_with_online_services > 0:
                # Increase online experience with decreasing social support for Black
                self.experience_with_online_services -= 0.03 * (self.last_social_support - self.social_support)

        if self.experience_with_online_services > 1:
            self.experience_with_online_services = 1
        if self.experience_with_online_services < 0:
            self.experience_with_online_services = 0

        # Print statements for debugging
        print(f"Agent {self.unique_id}")
        print(f"Step Count: {self.step_count}")
        print(f"Ethnicity: {self.ethnic}")
        print(f"Online Experience: {self.experience_with_online_services}")
        print(f"Social Support: {self.social_support}")
        print(f"Last Social Support: {self.last_social_support}")
        print("------")
