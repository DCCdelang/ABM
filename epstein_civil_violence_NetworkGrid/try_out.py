from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector
import random

#network
import networkx as nx
from mesa.space import NetworkGrid


def main():
    n_nodes = 10
    G = nx.barabasi_albert_graph(n_nodes, 5)
    grid = NetworkGrid(G)
     
    cops = random.sample(G.nodes(), int(0.3*n_nodes))
    
    print(grid.get_cell_list_contents(cops))

    for i, node in enumerate(G.nodes()):
        node = 'cop'

    print(grid.get_cell_list_contents([1,2]))
    





if __name__ == "__main__":
   main()
