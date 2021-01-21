import networkx as nx
import matplotlib.pyplot as plt


G = nx.barabasi_albert_graph(100, 6)
# self.G = nx.watts_strogatz_graph(self.N_agents, links, 6)
# relabel nodes, so only citizens are on it

options = {'node_color': 'green', 'node_size': 50, 'width': 0.1, "font_size": 7}

edges = []
mapping = {}
for i, g in enumerate(G.nodes):
    print(g, len(G.edges(g)))
    edges.append(len(G.edges(g))*10)
  

options = {'node_color': 'green', 'node_size': edges, 'width': 0.1, "font_size": 7}

nx.draw_spring(G, with_labels=False, font_weight='bold', **options)

plt.show()
raise ValueError()