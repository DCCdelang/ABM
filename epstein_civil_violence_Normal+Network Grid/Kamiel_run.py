#%%
import matplotlib.pyplot as plt
import importlib
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import sys
import seaborn as sns

from epstein_civil_violence.agent import Citizen, Cop
from epstein_civil_violence.model import EpsteinCivilViolence

import time

if len(sys.argv) <= 2:
    print("Usage: python kamiel_model_run.py Network Vision")
    exit()

network = sys.argv[1]
vision = int(sys.argv[2])
legitimacy_kind = np.array(["Fixed", "Global", "Local"]) # choose between "Fixed","Global","Local"
Legitimacy = "Local"
smart_cops = False
cop_density = .04

n_sim = 1
max_iters = 20000
sim_peak = []
percentage = 0
#for leg in legitimacy_kind:
for n in range(n_sim):
    #start = time.time()
    model = EpsteinCivilViolence(height=40, 
                        width=40, 
                        citizen_density=.7, 
                        cop_density=cop_density, 
                        citizen_vision=vision, 
                        cop_vision=7, 
                        legitimacy=.82, 
                        max_jail_term=30, 
                        max_iters=max_iters, # cap the number of steps the model takes
                        smart_cops = smart_cops,
                        legitimacy_kind = Legitimacy, # choose between "Fixed","Global","Local"
                        max_fighting_time=1,
                        network = network,
                        ) 
    model.run_model()
    percentage = (((n+1)/n_sim) * 100)
    print(f"{percentage}% Done")
    #finish = time.time()
    #print("Time =",finish-start)

    model_out = model.datacollector.get_model_vars_dataframe()
    agent_out = model.datacollector.get_agent_vars_dataframe()
    
    model_out.to_csv(f"Folder_{vision}/model_temp_{vision}_{network}_{Legitimacy}_{n}.csv")


# %%
