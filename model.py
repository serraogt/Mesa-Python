from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import HappinessAgent

class HappinessModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            a = HappinessAgent(i, self)
            self.schedule.add(a)

            # Add some agents to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()

# Example usage:
model = HappinessModel(100, 10, 10)
for _ in range(10):
    model.step()
