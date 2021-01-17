from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from .model import EpsteinCivilViolence
from .agent import Citizen, Cop

  
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule


COP_COLOR = "#800080"
AGENT_QUIET_COLOR = "#0066CC"
AGENT_REBEL_COLOR = "#CC0000"
AGENT_FIGHT_COLOR = "#52eb34"
JAIL_COLOR = "#757575"


def network_portrayal(G):
    # The model ensures there is 0 or 1 agent per node

    def node_color(agent):
        if not agent: 
            color =  "#000000"
        else:
            if len(agent) > 1:
                color =  AGENT_FIGHT_COLOR 

            elif type(agent[0]) is Citizen:
                color = (
                    AGENT_QUIET_COLOR if agent[0].condition == "Quiescent" else AGENT_REBEL_COLOR
                )
                color = JAIL_COLOR if agent[0].jail_sentence else color
                color = AGENT_FIGHT_COLOR if agent[0].condition == "Fighting" else color

            elif type(agent[0]) is Cop:
                color = COP_COLOR
        
        return color


    portrayal = dict()
    portrayal["nodes"] = [
        {
            "id": node_id,
            "size": 5 if agents else 2,
            "color": node_color(agents),
        
        }
        for (node_id, agents) in G.nodes.data("agent")
    ]

    portrayal["edges"] = [
        {
            "id": edge_id, 
            "source": source, 
            "target": target, 
            "color": "#000000"}
        for edge_id, (source, target) in enumerate(G.edges)
    ]

    return portrayal

network = NetworkModule(network_portrayal, 1000, 1000, library="d3")
chart = ChartModule(
    [{"Label": "Active", "Color": "Red"}], data_collector_name="datacollector"
)



model_params = dict(
    n_nodes=400,
    links=5,
    citizen_density=0.7,
    cop_density=0.04,
    citizen_vision=7,
    cop_vision=7,
    legitimacy=0.82,
    max_jail_term=30,
    smart_cops = False,
    max_fighting_time = 1
)


server = ModularServer(
    EpsteinCivilViolence, [network, chart], "Epstein Civil Violence", model_params
)
server.port = 8523

