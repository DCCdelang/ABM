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
problem = {
    'num_vars': 4,
    'names': ['links', 'citizen_vision', 'cop_vision', 'max_jail_term'],
    'bounds': [[1, 7], [1, 10], [1, 10], [1, 50]]
}

data_from_csv = pd.read_csv("Old_SA/SA_data_NAME.csv")
#%%
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


# %%
