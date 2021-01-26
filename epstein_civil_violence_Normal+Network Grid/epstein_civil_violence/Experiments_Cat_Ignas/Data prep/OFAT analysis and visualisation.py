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


for col in stats_data.columns: 
    print(col)
    sns.lineplot(data=stats_data, 
                 x="links", 
                 y=str(col),
                 ci = 95)
    plt.show()