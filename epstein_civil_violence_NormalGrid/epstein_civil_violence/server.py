from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from .model import EpsteinCivilViolence
from .agent import Citizen, Cop


COP_COLOR = "#000000"
AGENT_QUIET_COLOR = "#0066CC"
AGENT_REBEL_COLOR = "#CC0000"
AGENT_FIGHT_COLOR = "#52eb34"
JAIL_COLOR = "#757575"


def citizen_cop_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "x": agent.pos[0],
        "y": agent.pos[1],
        "Filled": "true",
    }

    if type(agent) is Citizen:
        color = (
            AGENT_QUIET_COLOR if agent.condition == "Quiescent" else AGENT_REBEL_COLOR
        )
        color = JAIL_COLOR if agent.jail_sentence else color
        color = AGENT_FIGHT_COLOR if agent.condition == "Fighting" else color
        portrayal["Color"] = color
        portrayal["r"] = 0.8
        portrayal["Layer"] = 0

    elif type(agent) is Cop:
        portrayal["Color"] = COP_COLOR
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
    return portrayal

legitimacy_kind = "Fixed" # choose between "Fixed","Global","Local"
smart_cops = True
cop_density = .04

model_params = dict(
    height=40, 
    width=40, 
    citizen_density=.7, 
    cop_density=cop_density, 
    citizen_vision=7, 
    cop_vision=7, 
    legitimacy=.82, 
    max_jail_term=30, 
    max_iters=500, # cap the number of steps the model takes
    smart_cops = smart_cops,
    legitimacy_kind = legitimacy_kind, # choose between "Fixed","Global","Local"
    max_fighting_time=1
)

canvas_element = CanvasGrid(citizen_cop_portrayal, 40, 40, 480, 480)
server = ModularServer(
    EpsteinCivilViolence, [canvas_element], "Epstein Civil Violence", model_params
)
