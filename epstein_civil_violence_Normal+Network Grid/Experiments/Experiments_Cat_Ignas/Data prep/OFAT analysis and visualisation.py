#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:42:25 2021

@author: IggyMac
"""

import seaborn as sns
from statistics_functions import give_stats_file
import matplotlib.pyplot as plt

path = '/Users/IggyMac/OneDrive - UvA/2020-2021/ABM/Project/epstein_civil_violence_Normal+Network Grid/OFAT - results'    

stats_data = give_stats_file(path)


stats_data_1 = stats_data[stats_data.links < 7]

stats_data_1 = stats_data_1.rename(columns={"frac_time_calm": "Fraction of time calm", 
                   "mean_peak_interval": "Mean peak interval",
                   "peaks": "Peaks",
                   "mean_peak_size": "Mean peak size"})

for col in stats_data_1.columns: 
    print(col)
    sns.lineplot(data=stats_data_1, 
                 x="links", 
                 y=str(col),
                 ci = 95)
    
    plt.xlabel("Links")
    plt.savefig(f"Figures/ofat_links_{col}.png")
    
    plt.show()