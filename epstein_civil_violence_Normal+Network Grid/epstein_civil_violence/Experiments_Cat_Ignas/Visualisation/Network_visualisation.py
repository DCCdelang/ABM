#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 22:18:21 2021

@author: IggyMac
"""

import networkx as nx
import matplotlib.pyplot as plt
from nxviz.plots import CircosPlot


er = nx.erdos_renyi_graph(1400, 0.3)
br = nx.barabasi_albert_graph(1400, 5)
c_er = CircosPlot(er)
c_er.draw()
plt.show()