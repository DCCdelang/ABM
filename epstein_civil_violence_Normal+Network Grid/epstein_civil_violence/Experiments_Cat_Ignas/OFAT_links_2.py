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
    'names': ['links'],
    'bounds': [1, 10]s
}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 3
max_steps = 10
distinct_samples = 10

# Set the outputs
model_reporters = {
            "mean_peak_size": lambda m: m.mean_peak_size(m),
            "std_peak_size": lambda m: m.std_peak_size(m),
            "mean_peak_interval": lambda m: m.mean_peak_interval(m),
            "std_peak_interval": lambda m: m.std_peak_interval(m),
            "perc_time_rebel": lambda m: m.perc_time_rebel(m),
            "perc_time_calm": lambda m: m.perc_time_calm(m),
            "Peaks": lambda m: m.count_peaks(m),
            "Legitimacy": lambda m: m.legitimacy_feedback,
            "DataCollector": lambda m: m.datacollector.get_model_vars_dataframe(),
        }


data = {}

for x in range(replicates):
    for i, var in enumerate(problem['names']):
        # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
        samples = np.linspace(problem['bounds'][0], problem['bounds'][1], num=distinct_samples)
        
        samples = [int(x) for x in samples]
        
        # Keep in mind that wolf_gain_from_food should be integers. You will have to change
        # your code to acommodate for this or sample in such a way that you only get integers.
        
        batch = BatchRunner(EpsteinCivilViolence, 
                            max_steps=max_steps,
                            iterations=1,
                            variable_parameters={var: samples},
                            model_reporters=model_reporters,
                            display_progress=True)
        
        batch.run_all()
        
        data[var] = batch.get_model_vars_dataframe()
    
batch.get_model_vars_dataframe()

    