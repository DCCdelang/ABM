
import matplotlib.pyplot as plt
import importlib
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import sys
import seaborn as sns

from epstein_civil_violence.agent import Citizen, Cop
from epstein_civil_violence.model import EpsteinCivilViolence

import time

legitimacy = "Global" # choose between "Fixed","Global","Local"
network = "Barabasi" # Choose between "Barabasi", "Renyi" and Small-world
max_iters = 200 # Choose for how many iterations you want the model to run


start = time.time()
model = EpsteinCivilViolence(height=40, 
                    width=40, 
                    citizen_density=.7, 
                    cop_density=0.04, 
                    citizen_vision=7, 
                    cop_vision=7, 
                    legitimacy=.82, 
                    max_jail_term=30, 
                    max_iters=max_iters, 
                    smart_cops = False,
                    legitimacy_kind = legitimacy, 
                    max_fighting_time=1,
                    network = network,
                    ) 
model.run_model()

# Showing the time it takes to run the model
finish = time.time()
print("Time =",finish-start)

# Getting the data from the data collector
model_out = model.datacollector.get_model_vars_dataframe()
agent_out = model.datacollector.get_agent_vars_dataframe()

# Shows the amount of active citizens and statistics
print("Mean amount of active citizens per step = ",model_out["Active"].mean())
print("Std of amount of active citizens per step = ",model_out["Active"].std())
print("Maximum of amount of active citizens in a time step = ",model_out["Active"].max())

# line 59 - 78 give back measured properties of the model
peaks, _ = find_peaks(model_out["Active"], height=50)
print("Indices of peaks:", peaks, "Amount:", len(peaks))

actives_list = model_out["Active"].to_list()
for peak in peaks:
    print("Peak of ", actives_list[peak], "citizens")

peak_intervals = []
if len(peaks)>1:
    for i in range(len(peaks)-1):
        peak_intervals.append(peaks[i+1] - peaks[i])
print("Peak intervals = ",peak_intervals)

time_between = []
time = 0
total_active = 0

count1, count2 = False, False
for i in range(1,len(actives_list)-1):
    if actives_list[i] < 50 and actives_list[i+1] >= 50:
        count1 = False
        time_between.append(time-1)
        time = 0
    if actives_list[i] >= 50 and actives_list[i+1] < 50:
        count1 = True
    if count1 == True:
        time += 1

print("Times of inter-outerbursts", time_between)

# Makes a plot of the state of the citizens
ax = model_out[["Quiescent","Active", "Jailed", "Fighting"]].plot()
ax.set_title('Citizen Condition Over Time')
ax.set_xlabel('Step')
ax.set_ylabel('Number of Citizens')
_ = ax.legend(bbox_to_anchor=(1.35, 1.025))
plt.tight_layout()

plt.show()

# Makes a plot of perceived legitimacy
if legitimacy != "Local":
    ax = model_out[["Legitimacy"]].plot()
    ax.set_title('Citizen Condition Over Time')
    ax.set_xlabel('Step')
    ax.set_ylabel('Number of Citizens')
    _ = ax.legend(bbox_to_anchor=(1.35, 1.025))
    plt.tight_layout()
    plt.show()


print(agent_out[["breed","Legitimacy"]].filter(like='1040', axis = 0 ).head())
print(agent_out[["breed","Legitimacy"]].filter(like='1041', axis = 0 ).head())
print(agent_out[["breed","Legitimacy"]].filter(like='1042', axis = 0 ).head())

if legitimacy == "Local":
    ax = agent_out["Legitimacy"].filter(like='1040', axis = 0 ).plot()
    ax.set_title('Citizen Condition Over Time')
    ax.set_xlabel('Step')
    ax.set_ylabel('Number of Citizens')
    _ = ax.legend(bbox_to_anchor=(1.35, 1.025))
   
    plt.tight_layout()
    plt.show()