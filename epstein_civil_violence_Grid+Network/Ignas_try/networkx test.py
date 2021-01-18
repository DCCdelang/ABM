import networkx as nx
import matplotlib.pyplot as plt
import statsmodels
import mesa

ws = nx.watts_strogatz_graph(150, 4, 0.1)
ba = nx.barabasi_albert_graph(20, 4)

nx.draw_kamada_kawai(ws, with_labels=True, font_weight='bold')