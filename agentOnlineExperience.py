from mesa import Agent
import random
from openpyxl import Workbook, load_workbook
import pandas as pd

class CustomerOnlineExperienceAgent(Agent):

    df = pd.read_excel('PopulatioDataEncoded.xlsx')

    """ I will not use that technique for now
    book = load_workbook('PopulationDataEncoded.xlsx')
    sheet = book.active #will be useful if there is multiple sheets
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        #self.age = self.random.randint(18, 80) not used yet
        self.ethnic = self.get_ethnicity() #denendi okay
        self.step_count = 0
        self.social_support = 0.5 #self.get_social_support()
        self.social_support_change = 0
        self.spoken_english = self.get_initial_speaking()
        # it is something to decide
        
    def get_initial_speaking(self):

        speaking_list = (list)(self.df[self.df.columns[11]].values)

        initial_speaking=speaking_list[self.unique_id]

        return initial_speaking
        
        """ old version
        if self.ethnic == "White":
            return random.choice([0.4, 0, -0.5, 0.5, 0.5, 0]) * 1.0  # Choose from 1 or 0 for more positive values
        elif self.ethnic == "Asian":
            return random.choice([-0.5, 0, 0.4, 0]) * 1.0 # Choose from -1, 0, or 1 for a balanced range
        else:
            return random.choice([0, -0.5, 0, -0.5, -0.1, 0.1]) * 1.0 # Choose from 0 or 1 for more positive values """

    def get_social_support(self):
        # Set social support based on ethnicity
        if self.ethnic == "White":
            return self.random.uniform(0.0, 0.1)
        elif self.ethnic == "Asian":
            return self.random.uniform(0.1, 0.2)
        else:
            return self.random.uniform(0.2, 0.3)
        
    def get_ethnicity(self):
        #return self.sheet['C2'].values

        ethnicity_list = (list)(CustomerOnlineExperienceAgent.df["Ethnic Group"].values)
       
        self.ethnic=ethnicity_list[self.unique_id]

        """
        # Assign ethnic based on probabilities
        rand_num = random.uniform(0, 1)
        if rand_num < 0.3:
            return "Asian"
        elif rand_num < 0.6:
            return "Black"
        else:
            return "White" 
            """

    def step(self): #races get effected differently from same social support
        self.step_count += 1
        
        #will be given by machine learning algorithm
        # change spoken english level according to social support change
        if self.ethnic == "0":
            self.spoken_english += 0.1 * self.social_support
        elif self.ethnic == "1": 
            self.spoken_english += 0.2 * self.social_support
        else:
            self.spoken_english += 0.3 * self.social_support

        # Set last social support to the current social support for the next step
        self.last_social_support = self.social_support

        # Ensure the experience is within the valid range
        self.spoken_english  = max(-1, min(3, self.spoken_english))

        # Print two statements for debugging
        if self.step_count==0 or self.step_count==4:
            print(f"Agent {self.unique_id}")
            print(f"Step Count: {self.step_count}")
            print(f"Ethnicity: {self.ethnic}")
            print(f"Learning Experience: {self.spoken_english}")
            print(f"Social Support: {self.social_support}")
            print(f"Social Support Change: {self.social_support_change}")
            print("------")