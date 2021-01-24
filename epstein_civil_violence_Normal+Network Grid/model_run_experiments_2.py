#%%
import matplotlib.pyplot as plt
import importlib
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import seaborn as sns

from epstein_civil_violence.agent import Citizen, Cop
from epstein_civil_violence.model import EpsteinCivilViolence

import time
legitimacy_kind = np.array(["Fixed", "Global", "Local"]) # choose between "Fixed","Global","Local"
leg = legitimacy_kind = "Fixed"
smart_cops = False
cop_density = .04

n_sim = 6
max_iters = 100
sim_peak = []
#for leg in legitimacy_kind:
for n in range(n_sim):
    #start = time.time()
    model = EpsteinCivilViolence(height=40, 
                           width=40, 
                           citizen_density=.7, 
                           cop_density=cop_density, 
                           citizen_vision=7, 
                           cop_vision=7, 
                           legitimacy=.82, 
                           max_jail_term=30, 
                           max_iters=max_iters, # cap the number of steps the model takes
                           smart_cops = smart_cops,
                           legitimacy_kind = leg, # choose between "Fixed","Global","Local"
                           max_fighting_time=1
                           ) 
    model.run_model()

    #finish = time.time()
    #print("Time =",finish-start)

    model_out = model.datacollector.get_model_vars_dataframe()
    agent_out = model.datacollector.get_agent_vars_dataframe()

    model_out.to_csv(f"model_temp_{legitimacy_kind}_{n}.csv")
    agent_out.to_csv(f"agent_temp_{legitimacy_kind}_{n}.csv")



    model_out = pd.read_csv(f"model_temp_{legitimacy_kind}_{n}.csv")

    #print(model_out["Active"].mean())
    #print(model_out["Active"].std())
    #print(model_out["Active"].max())

    peaks= find_peaks(model_out["Active"], height=50)
    #print("Indices of peaks:", peaks, "Amount:", len(peaks))

    # save number of peaks
    sim_peak.append(len(peaks))


"""
    actives_list = model_out["Active"].to_list(len(peaks))

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
        # if actives_list[i] < 50 and actives_list[i+1] >= 50:
        #     count2 = True
        # if count2 == True:
        #     total_active += actives_list[i+1]

        # if actives_list[i] >= 50 and actives_list[i+1] < 50:
        #     count1 = False
        #     time_between.append(time-1)
        #     time = 0
    #print("Times of inter-outerbursts", time_between)
"""
frames = []
distribution = []

for n in range(n_sim):
    model_out = pd.read_csv(f"model_temp_{legitimacy_kind}_{n}.csv")
    print(n)
    if n > 0:
        model_out.drop([0])
    frames.append(model_out)

result = pd.concat(frames)

y = result["Active"]
print(y)

print(result)


sns.lineplot(data=result, x="Unnamed: 0", y="Active")
sns.lineplot(data=result, x="Unnamed: 0", y="Fighting")
sns.lineplot(data=result, x="Unnamed: 0", y="Quiescent")
sns.lineplot(data=result, x="Unnamed: 0", y="Jailed")

plt.show()


# %%
