from mesa import Agent
import random

class CustomerNewAgent(Agent):
    """An agent with initial happiness"""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.age = self.random.randint(18, 80)
        self.discriminated = 0.9
        self.ethnic = self.get_ethnicity()
        self.step_count = 0
        self.social_support = 0.1
        self.last_social_support = self.get_social_support()

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
            if self.discriminated < 1 and self.discriminated > 0:
                # Decrease discrimination with increasing social support for White
                self.discriminated -= 0.01 * (self.last_social_support - self.social_support)

        elif self.ethnic == "Asian":
               self.discriminated -= 0.02 * (self.last_social_support - self.social_support)
        else:
            if self.discriminated < 1 and self.discriminated > 0:
                # Increase discrimination with decreasing social support for Black
                self.discriminated -= 0.03 * (self.last_social_support - self.social_support)

        if self.discriminated > 1:
            self.discriminated = 1
        if self.discriminated < 0: 
            self.discriminated = 0

        # Print statements for debugging
        print(f"Agent {self.unique_id}")
        print(f"Step Count: {self.step_count}")
        print(f"Ethnicity: {self.ethnic}")
        print(f"Discriminated: {self.discriminated}")
        print(f"Social Support: {self.social_support}")
        print(f"Last Social Support: {self.last_social_support}")
        print("------")
