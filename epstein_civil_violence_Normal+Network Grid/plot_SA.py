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
# param_Cat = param_values[0:120]
# param_Dante = param_values[180:200] # 140,160,180,200,220,240
# param_Kamiel = param_values[240:360]
# param_Louky = param_values[360:480]
# param_Ignas = param_values[480:]

cat_1 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Cat/SA_data_Cat_1/SA_data_Cat_1.csv")
cat_2 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Cat/SA_data_Cat_2/SA_data_Cat_2.csv")
cat_3 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Cat/SA_data_Cat_3/SA_data_Cat_3.csv")
cat_4 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Cat/SA_data_Cat_4/SA_data_Cat_4.csv")
cat_5 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Cat/SA_data_Cat_5/SA_data_Cat_5.csv")
cat_6 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Cat/SA_data_Cat_6/SA_data_Cat_6.csv")

Cat_Total = pd.concat([cat_1,cat_2,cat_3,cat_4,cat_5,cat_6])
print(Cat_Total.shape)

dante_1 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Dante/SA_data_120_140.csv")
dante_2 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Dante/SA_data_140_160.csv")
dante_3 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Dante/SA_data_160_180.csv")
dante_4 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Dante/SA_data_180_200.csv")
dante_5 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Dante/SA_data_200_220.csv")
dante_6 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Dante/SA_data_220_240.csv")

Dante_Total = pd.concat([dante_1,dante_2,dante_3,dante_4,dante_5,dante_6])
print(Dante_Total.shape)

iggy_1 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Iggy/SA_data1.csv")
iggy_2 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Iggy/SA_data2.csv")
iggy_3 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Iggy/SA_data3.csv")
iggy_4 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Iggy/SA_data4.csv")
iggy_5 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Iggy/SA_data5.csv")
iggy_6 = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Iggy/SA_data6.csv")

Iggy_Total = pd.concat([iggy_1,iggy_2,iggy_3,iggy_4,iggy_5,iggy_6])
print(Iggy_Total.shape)

Kamiel_Total = pd.read_csv("epstein_civil_violence_Normal+Network Grid/SA_data_Kamiel/SA_data_Kamiel.csv")
print(Kamiel_Total.shape)

Total_SA = pd.concat([Cat_Total,Dante_Total,Iggy_Total,Kamiel_Total]).fillna(0)
print(Total_SA.shape)
print(Total_SA.head())
#%%
Si_active = sobol.analyze(problem, Total_SA['perc_time_rebel'].values, print_to_console=True, calc_second_order=False)
Si_calm = sobol.analyze(problem, Total_SA['perc_time_calm'].values, print_to_console=True, calc_second_order=False)
Si_legitimacy = sobol.analyze(problem, Total_SA['mean_peak_size'].values, print_to_console=True, calc_second_order=False)
Si_peak_interval = sobol.analyze(problem, Total_SA['mean_peak_interval'].values, print_to_console=True, calc_second_order=False)
Si_peaks = sobol.analyze(problem, Total_SA['Peaks'].values, print_to_console=True, calc_second_order=False)

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

Si = [Si_active, Si_calm, Si_legitimacy, Si_peaks, Si_peak_interval]
title = ["Si_active", "Si_calm", "Si_legitimacy", "Si_peaks", "Si_peak_interval"]

for i in range(len(Si)):
    # First order
    plot_index(Si[i], problem['names'], '1', 'First order '+title[i])
    plt.show()

    # Total order
    plot_index(Si[i], problem['names'], 'T', 'Total order '+title[i])
    plt.show()
