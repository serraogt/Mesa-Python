from mesa import Model
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import HappinessModel


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if agent.getHappiness() == 0.5:
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.4
    elif agent.getHappiness() > 0.5:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
    elif agent.getHappiness() < 0.5:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.2

    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(HappinessModel, [grid], "Happiness Model", {"N":100, "width":10, "height":10})
server.port = 8521  # You can change the port if needed
server.launch()
