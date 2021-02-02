#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:42:25 2021

@author: IggyMac
"""
import os

os.chdir("/Users/IggyMac/OneDrive - UvA/2020-2021/ABM/Project/epstein_civil_violence_Normal+Network Grid/epstein_civil_violence/Experiments_Cat_Ignas/Data prep")

import seaborn as sns
from statistics_functions import give_stats_file
import matplotlib.pyplot as plt

path = '/Users/IggyMac/OneDrive - UvA/2020-2021/ABM/Project/epstein_civil_violence_Normal+Network Grid/OFAT - results - cop_vision'    

stats_data = give_stats_file(path)


stats_data_1 = stats_data[stats_data.cop_vision < 9] 

stats_data_1 = stats_data_1.rename(columns={"frac_time_calm": "Fraction of time calm", 
                   "mean_peak_interval": "Mean peak interval",
                   "peaks": "Peaks",
                   "mean_peak_size": "Mean peak size"})

for col in stats_data_1.columns: 
    print(col)
    sns.lineplot(data=stats_data_1, 
                 x="cop_vision", 
                 y=str(col),
                 ci = 95)
    plt.xlabel("Cop vision")
    plt.savefig(f"Figures/ofat_c_v_{col}.png")
    plt.show()
