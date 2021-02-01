#%%
import matplotlib.pyplot as plt
import importlib
import pandas as pd
from scipy.signal import find_peaks

from epstein_civil_violence.agent import Citizen, Cop
from epstein_civil_violence.model import EpsteinCivilViolence

import time
legitimacy_kind = "Fixed" # choose between "Fixed","Global","Local"
smart_cops = True
cop_density = .04

start = time.time()
model = EpsteinCivilViolence(height=40, 
                           width=40, 
                           citizen_density=.7, 
                           cop_density=cop_density, 
                           citizen_vision=7, 
                           cop_vision=7, 
                           legitimacy=.82, 
                           max_jail_term=30, 
                           max_iters=20, # cap the number of steps the model takes
                           smart_cops = smart_cops,
                           legitimacy_kind = legitimacy_kind, # choose between "Fixed","Global","Local"
                           max_fighting_time=1
                           ) 
model.run_model()

finish = time.time()
print("Time =",finish-start)

model_out = model.datacollector.get_model_vars_dataframe()
agent_out = model.datacollector.get_agent_vars_dataframe()

model_out.to_csv("CSV_temp/model_temp.csv")
agent_out.to_csv("CSV_temp/agent_temp.csv")

#%%
model_out = pd.read_csv("CSV_temp/model_temp.csv")

print(model_out["Active"].mean())
print(model_out["Active"].std())
print(model_out["Active"].max())

peaks, _ = find_peaks(model_out["Active"], height=50)
print("Indices of peaks:", peaks, "Amount:", len(peaks))

actives_list = model_out["Active"].to_list()
for peak in peaks:
    print(peak, actives_list[peak])
print(actives_list)

peak_intervals = []
if len(peaks)>1:
    for i in range(len(peaks)-1):
        peak_intervals.append(peaks[i+1] - peaks[i])
print(peak_intervals)

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
print("Times of inter-outerbursts", time_between)
exit()

# %%

#%%
# model_out = pd.read_csv("C:/Users/djdcc/Documents/School/UNI/Computational Science/Agent Based Modelling/ABM/epstein_civil_violence_Normal+Network Grid/SA_data/0_2_1_5_34-0_iteration.csv")
ax = model_out[["Quiescent","Active", "Jailed", "Fighting"]].plot()
ax.set_title('Citizen Condition Over Time')
ax.set_xlabel('Step')
ax.set_ylabel('Number of Citizens')
_ = ax.legend(bbox_to_anchor=(1.35, 1.025))
plt.tight_layout()
# plt.savefig("figures_normalgrid/plot_"+legitimacy_kind+"_"+str(cop_density)+"_"+str(smart_cops)+".png")
plt.show()
if legitimacy_kind != "Local":
    ax = model_out[["Legitimacy"]].plot()
    ax.set_title('Citizen Condition Over Time')
    ax.set_xlabel('Step')
    ax.set_ylabel('Number of Citizens')
    _ = ax.legend(bbox_to_anchor=(1.35, 1.025))
    plt.tight_layout()
    # plt.savefig("figures_normalgrid/legit_"+legitimacy_kind+"_"+str(cop_density)+"_"+str(smart_cops)+".png")
    plt.show()


print(agent_out[["breed","Legitimacy"]].filter(like='1040', axis = 0 ).head())
print(agent_out[["breed","Legitimacy"]].filter(like='1041', axis = 0 ).head())
print(agent_out[["breed","Legitimacy"]].filter(like='1042', axis = 0 ).head())

if legitimacy_kind == "Local":
    ax = agent_out["Legitimacy"].filter(like='1040', axis = 0 ).plot()
    ax.set_title('Citizen Condition Over Time')
    ax.set_xlabel('Step')
    ax.set_ylabel('Number of Citizens')
    _ = ax.legend(bbox_to_anchor=(1.35, 1.025))
    # plt.savefig("figures_normalgrid/legit_"+legitimacy_kind+"_"+str(cop_density)+"_"+str(smart_cops)+".png")
    plt.tight_layout()
    plt.show()

# single_agent_out = agent_out[single_agent]
# single_agent_out.head()

# %%
