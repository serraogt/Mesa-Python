from mesa import Model
from agent import MoneyAgent
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import MoneyModel


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if agent.wealth == 0:
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.4
    elif agent.wealth > 0:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    elif agent.wealth < 0:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.2

    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(MoneyModel, [grid], "Money Model", {"N":100, "width":10, "height":10})
server.port = 8521  # You can change the port if needed
server.launch()
