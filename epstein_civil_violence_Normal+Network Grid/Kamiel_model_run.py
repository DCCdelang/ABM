#%%
import matplotlib.pyplot as plt
import importlib
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import seaborn as sns

from epstein_civil_violence.agent import Citizen, Cop
from epstein_civil_violence.model import EpsteinCivilViolence

import time
legitimacy_kind = np.array(["Fixed", "Global", "Local"]) # choose between "Fixed","Global","Local"
leg = legitimacy_kind = "Global"
smart_cops = False
cop_density = .04

n_sim = 300
max_iters = 50
sim_peak = []
percentage = 0
#for leg in legitimacy_kind:
networks = ["Barabasi", "Renyi", "Small-world"]
for n in range(n_sim):
    for network in networks:
        #start = time.time()
        model = EpsteinCivilViolence(height=40, 
                            width=40, 
                            citizen_density=.7, 
                            cop_density=cop_density, 
                            citizen_vision=7, 
                            cop_vision=7, 
                            legitimacy=.82, 
                            max_jail_term=30, 
                            max_iters=max_iters, # cap the number of steps the model takes
                            smart_cops = smart_cops,
                            legitimacy_kind = leg, # choose between "Fixed","Global","Local"
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
        
        model_out.to_csv(f"epstein_civil_violence_Normal+Network Grid/Data/model_temp_{network}_{legitimacy_kind}_{n}.csv")

        model_out = pd.read_csv(f"epstein_civil_violence_Normal+Network Grid/Data/model_temp_{network}_{legitimacy_kind}_{n}.csv")



# %%
