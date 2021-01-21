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

from epstein_civil_violence.agent import Citizen, Cop
from epstein_civil_violence.model import EpsteinCivilViolence

problem = {
    'num_vars': 4,
    'names': ['links', 'citizen_vision', 'cop_vision', 'max_jail_term'],
    'bounds': [[1, 10], [1, 20], [1, 20], [1, 50]]
}

#%%
# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 2 # Will be 5
max_steps = 20 # Will be 500 (?)
distinct_samples = 3 # Will be 100

param_values = saltelli.sample(problem, distinct_samples, calc_second_order=False)

model_reporters = {
            "Quiescent": lambda m: m.count_type_citizens(m, "Quiescent"),
            "Active": lambda m: m.count_type_citizens(m, "Active"),
            "Jailed": lambda m: m.count_jailed(m),
            "Fighting": lambda m: m.count_fighting(m),
            "Peaks": lambda m: m.count_peaks(m),
            "Legitimacy": lambda m: m.legitimacy_feedback,
        }

batch = BatchRunner(EpsteinCivilViolence,
                    max_steps=max_steps,
                    variable_parameters={name:[] for name in problem['names']},
                    model_reporters=model_reporters)

count = 0
data = pd.DataFrame(index=range(replicates*len(param_values)), 
                                columns=['links', 'citizen_vision', 'cop_vision', 'max_jail_term'])
data['Run'], data['Quiescent'], data['Active'], data['Jailed'], data['Fighting'], data['Legitimacy'],  data['Peaks'] = None, None, None, None, None, None, None

start = time.time()
for i in range(replicates):
    for vals in param_values:
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
        iteration_data['Run'] = count # Don't know what causes this, but iteration number is not correctly filled
        data.iloc[count, 0:4] = vals
        data.iloc[count, 4:11] = iteration_data
        count += 1
        end = time.time() - start
        print("One run", end)

        print(f'{count / (len(param_values) * (replicates)) * 100:.2f}% done')

# print(param_values)
print(len(param_values))
print(data)

data.to_csv("SA_data.csv")

#%%
data_from_csv = pd.read_csv("SA_data.csv")

Si_active = sobol.analyze(problem, data_from_csv['Active'].values, print_to_console=True, calc_second_order=False)
Si_legitimacy = sobol.analyze(problem, data_from_csv['Legitimacy'].values, print_to_console=True, calc_second_order=False)
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
# %%
