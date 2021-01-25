#%%
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

problem = {
    'num_vars': 4,
    'names': ['links', 'citizen_vision', 'cop_vision', 'max_jail_term'],
    'bounds': [[1, 7], [1, 10], [1, 10], [1, 50]]
}
#%%
# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 5 # Will be 5
max_steps = 400 # Will be 400 (?)
distinct_samples = 100 # Will be 100

param_values = saltelli.sample(problem, distinct_samples, calc_second_order=False)

param_Cat = param_values[0:120]
param_Dante = param_values[180:200] # 140,160,180,200,220,240
param_Kamiel = param_values[240:360]
param_Louky = param_values[360:480]
param_Ignas = param_values[480:]
# print(param_Dante)
# print(len(param_Cat),len(param_Dante),len(param_Kamiel))

"""Choose your param set and set file name <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"""
<<<<<<< HEAD
param_values = param_Louky
data_file_name = r"C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block3\ABM\epstein_civil_violence_Normal+Network Grid\SA_data_Louky\SA_data.csv"

=======
# param_values = param_Dante
data_file_name = "epstein_civil_violence_Normal+Network Grid/SA_data/SA_data_NAME.csv"
>>>>>>> 88f0344c9baecc7aa1a909592681b10c18c00a58

#%%
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

batch = BatchRunner(EpsteinCivilViolence,
                    max_steps=max_steps,
                    variable_parameters={name:[] for name in problem['names']},
                    model_reporters=model_reporters)

count = 0
title_count = 0
data = pd.DataFrame(index=range(replicates*len(param_values)), 
                                columns=['links', 'citizen_vision', 'cop_vision', 'max_jail_term'])

data['Run'], data['mean_peak_size'], data['std_peak_size'], data['mean_peak_interval'], data['std_peak_interval'], data['perc_time_rebel'],  data['perc_time_calm'], data['Legitimacy'],  data['Peaks']= None, None, None, None, None, None, None, None, None

total_start = time.time()
for vals in param_values:
    for i in range(replicates):
        start = time.time()
        # if count > 88: # Computer crashed
        # Change parameters that should be integers
        vals = list(vals)
        vals[0] = int(vals[0])
        vals[1] = int(vals[1])
        vals[2] = int(vals[2])
        vals[3] = int(vals[3])
        # Transform to dict with parameter names and their values
        variable_parameters = {}
        for name, val in zip(problem['names'], vals):
            variable_parameters[name] = val
        # print("Workie?\n", count)
        print(variable_parameters)
        batch.run_iteration(variable_parameters, tuple(vals), count)
        iteration_data = batch.get_model_vars_dataframe().iloc[count]

        iteration_data['Run'] = title_count # Don't know what causes this, but iteration number is not correctly filled
        data.iloc[count, 0:4] = vals
        data.iloc[count, 4:] = iteration_data
        title = str(title_count)
        for value in vals:
            title = title + "_" + str(value)
        # print(data)
        # print(iteration_data) # Apparently the second row is the dataframe
<<<<<<< HEAD
        
        iteration_data[1].to_csv(r"C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block3\ABM\epstein_civil_violence_Normal+Network Grid\SA_data_Louky\SA_" + title + "-" + str(i)+"_iteration.csv")
=======
        iteration_data[1].to_csv("epstein_civil_violence_Normal+Network Grid/SA_data/" + title + "-" + str(i)+"_iteration.csv")
>>>>>>> 88f0344c9baecc7aa1a909592681b10c18c00a58
        # data['DataCollector'] = None
        count += 1
        title_count += 1
        end = time.time() - start
        print("Time one run", end)
        print(f'{count / (len(param_values) * (replicates)) * 100:.2f}% done\n')
        data.to_csv(data_file_name)
        # exit()

total_end = time.time() - total_start
print("Total time",total_end)
# print(param_values)
print(data)
data.to_csv(data_file_name)

exit()
