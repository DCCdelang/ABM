#%%
import matplotlib.pyplot as plt
import importlib
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from epstein_civil_violence.model import EpsteinCivilViolence
from epstein_civil_violence.agent import Citizen, Cop

import time
leg = legitimacy_kind = "Local" # choose between "Fixed","Global","Local"
smart_cops = False
cop_density = .04

start = time.time()
model = EpsteinCivilViolence(height=40, 
                           width=40,
                           links = 5,
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
# model_out.head(5)
model_out.to_csv(f"CSV_temp/model_temp_{leg}.csv")
agent_out.to_csv(f"CSV_temp/agent_temp_{leg}.csv")

ax = model_out[["Quiescent","Active", "Jailed", "Fighting"]].plot()
ax.set_title(f'Citizen Condition Over Time - {leg}')
ax.set_xlabel('Step')
ax.set_ylabel('Number of Citizens')
_ = ax.legend(bbox_to_anchor=(1.35, 1.025))
plt.tight_layout()
plt.savefig(f"figures_normalnet/plot_{leg}_.png")
plt.show()

if legitimacy_kind != "Local":
    ax = model_out[["Legitimacy"]].plot()
    ax.set_title('Citizen Condition Over Time')
    ax.set_xlabel('Step')
    ax.set_ylabel('Number of Citizens')
    _ = ax.legend(bbox_to_anchor=(1.35, 1.025))
    plt.tight_layout()
    plt.savefig("figures_normalgrid/legit_"+legitimacy_kind+"_"+str(cop_density)+"_"+str(smart_cops)+".png")
    plt.show()

agent_out = model.datacollector.get_agent_vars_dataframe()
#%%
agent_out.head(5)
# like_list = ['1244','1243']
print(agent_out[["breed","Legitimacy"]].filter(like='1040', axis = 0 ).head())
print(agent_out[["breed","Legitimacy"]].filter(like='1041', axis = 0 ).head())
print(agent_out[["breed","Legitimacy"]].filter(like='1042', axis = 0 ).head())

if legitimacy_kind == "Local":
    ax = agent_out["Legitimacy"].filter(like='1040', axis = 0 ).plot()
    ax.set_title('Citizen Condition Over Time')
    ax.set_xlabel('Step')
    ax.set_ylabel('Number of Citizens')
    _ = ax.legend(bbox_to_anchor=(1.35, 1.025))
    plt.savefig("figures_normalgrid/legit_"+legitimacy_kind+"_"+str(cop_density)+"_"+str(smart_cops)+".png")
    plt.tight_layout()
    plt.show()