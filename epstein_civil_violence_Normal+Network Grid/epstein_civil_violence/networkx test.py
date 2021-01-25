#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 12:49:54 2021

@author: IggyMac
"""

import networkx as nx

# initialise network

G = nx.barabasi_albert_graph(1200, 5)

# get neighbors of the agent

neighbors = list(nx.all_neighbors(G, 1))

# go throught the list of agents and calculate the number of fighting agents

fighting = 0
itteration = 0

# count the number of active agents

for citizen in self.model.schedule.agents:
    if citizen.unique_id == neighbors[itteration] and citizen.condition == "Active":
        fighting += 1
        itteration += 1
    if itteration > len(neighbors) - 1:
        break
        
    
    