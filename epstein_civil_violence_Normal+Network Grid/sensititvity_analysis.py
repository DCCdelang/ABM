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
print(len(param_values))

param_Cat = param_values[0:120]
param_Dante = param_values[120:240]
param_Kamiel = param_values[240:360]
param_Louky = param_values[360:480]
param_Ignas = param_values[480:]
# print(param_Dante)
# print(len(param_Cat),len(param_Dante),len(param_Kamiel))

"""Choose your param set and set file name <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"""
param_values = param_Louky
data_file_name = r"C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block3\ABM\epstein_civil_violence_Normal+Network Grid\SA_data_Louky\SA_data.csv"


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
data = pd.DataFrame(index=range(replicates*len(param_values)), 
                                columns=['links', 'citizen_vision', 'cop_vision', 'max_jail_term'])

data['Run'], data['mean_peak_size'], data['std_peak_size'], data['mean_peak_interval'], data['std_peak_interval'], data['perc_time_rebel'],  data['perc_time_calm'], data['Legitimacy'],  data['Peaks']= None, None, None, None, None, None, None, None, None

total_start = time.time()
for i in range(replicates):
    for vals in param_values:
        start = time.time()
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
        print(variable_parameters)
        batch.run_iteration(variable_parameters, tuple(vals), count)
        iteration_data = batch.get_model_vars_dataframe().iloc[count]
        
        print(data)
        print(iteration_data)
        iteration_data['Run'] = count # Don't know what causes this, but iteration number is not correctly filled
        data.iloc[count, 0:4] = vals
        data.iloc[count, 4:] = iteration_data
        title = str(count)
        for value in vals:
            title = title + "_" + str(value)
        # print(data)
        # print(iteration_data) # Apparently the second row is the dataframe
        
        iteration_data[1].to_csv(r"C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block3\ABM\epstein_civil_violence_Normal+Network Grid\SA_data_Louky\SA_" + title + "-" + str(i)+"_iteration.csv")
        # data['DataCollector'] = None
        count += 1
        end = time.time() - start
        print("Time one run", end)
        print(f'{count / (len(param_values) * (replicates)) * 100:.2f}% done\n')
        data.to_csv(data_file_name)

total_end = time.time() - total_start
print("Total time",total_end)
# print(param_values)
print(data)

exit()
#%%
data_from_csv = pd.read_csv("SA_data/SA_data.csv")

Si_active = sobol.analyze(problem, data_from_csv['perc_time_rebel'].values, print_to_console=True, calc_second_order=False)
Si_legitimacy = sobol.analyze(problem, data_from_csv['mean_peak_size'].values, print_to_console=True, calc_second_order=False)
Si_peaks = sobol.analyze(problem, data_from_csv['Peaks'].values, print_to_console=True, calc_second_order=False)
Si_peaks = sobol.analyze(problem, data_from_csv['Peaks'].values, print_to_console=True, calc_second_order=False)

def plot_index(s, params, i, title=''):
    """
    Creates a plot for Sobol sensitivity analysis that shows the contributions
    of each parameter to the global sensitivity.

    Args:
        s (dict): dictionary {'S#': dict, 'S#_conf': dict} of dicts that hold
            the values for a set of parameters
        params (list): the parameters taken from s
        i (str): string that indicates what order the sensitivity is.
        title (str): title for the plot
    """

    if i == '2':
        p = len(params)
        params = list(combinations(params, 2))
        indices = s['S' + i].reshape((p ** 2))
        indices = indices[~np.isnan(indices)]
        errors = s['S' + i + '_conf'].reshape((p ** 2))
        errors = errors[~np.isnan(errors)]
    else:
        indices = s['S' + i]
        errors = s['S' + i + '_conf']
        plt.figure()

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')

for Si in (Si_active, Si_legitimacy, Si_peaks):
    # First order
    plot_index(Si, problem['names'], '1', 'First order sensitivity')
    plt.show()

    # Total order
    plot_index(Si, problem['names'], 'T', 'Total order sensitivity')
    plt.show()

