node_list = list(self.G.nodes)
random.shuffle(self.citizen_ids)
mapping = dict(zip(node_list, self.citizen_ids))
self.G = nx.relabel_nodes(self.G, mapping)

self.running = True
self.datacollector.collect(self)


new_map = {}
edges = []
for g in self.G.nodes:
    edges.append(len(self.G.edges(g))*1)

options = {'node_color': 'green', 'node_size': edges, 'width': 0.2, "font_size": 6, 'font_color': "red"}
nx.draw(self.G, with_labels=False, font_weight='bold', **options)
plt.show()