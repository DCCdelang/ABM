import os

os.chdir('/Users/IggyMac/OneDrive - UvA/2020-2021/ABM/Project/epstein_civil_violence_Normal+Network Grid')

import SALib
from SALib.sample import saltelli
from mesa.batchrunner import BatchRunner
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import time
#%%
from epstein_civil_violence.agent import Citizen, Cop
from epstein_civil_violence.model import EpsteinCivilViolence


# We define our variables and bounds
problem = {
    'num_vars': 1,
    'names': ['cop_vision'],
    'bounds': [1, 10]
}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 10
max_steps = 400
distinct_samples = 10


samples = np.linspace(problem['bounds'][0], problem['bounds'][1], num=distinct_samples)
samples = [int(x) for x in samples]
sample = samples[2]

for i in range(replicates):
    
    print(i)
    print(sample)

    model = EpsteinCivilViolence(cop_vision = sample,
                                 max_iters = max_steps)
    model.run_model()

    data = model.datacollector.get_model_vars_dataframe()
    
    data["cop_vision"] = sample
    data["run"] = i
    
    data.to_csv(f"OFAT - results - cop_vision/OFAT - cop_vision({sample}) - run({i}).csv")
    
    print(data)
    

        



    