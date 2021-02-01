import matplotlib.pyplot as plt
import importlib

from epstein_civil_violence.model import EpsteinCivilViolence
from epstein_civil_violence.agent import Citizen, Cop

import time
legitimacy_kind = "Global" # choose between "Fixed","Global","Local"
smart_cops = False
cop_density = .04

start = time.time()
<<<<<<< HEAD
model = EpsteinCivilViolence(height=40, 
                           width=40,
=======
model = EpsteinCivilViolence(height=100, 
                           width=100,
>>>>>>> 999953f52a88c79d3a33d0b48892d4544ca4c12b
                           links = 10,
                           citizen_density=.7, 
                           cop_density=0.04, 
                           citizen_vision=7, 
                           cop_vision=7, 
                           legitimacy=.82, 
                           max_jail_term=30, 
<<<<<<< HEAD
                           max_iters=100, # cap the number of steps the model takes
                           smart_cops = smart_cops,
=======
                           max_iters=180, # cap the number of steps the model takes
                           smart_cops = False,
>>>>>>> 999953f52a88c79d3a33d0b48892d4544ca4c12b
                           legitimacy_kind = legitimacy_kind, # choose between "Fixed","Global","Local"
                           max_fighting_time=1
                           ) 
model.run_model()

finish = time.time()
print("Time =",finish-start)

model_out = model.datacollector.get_model_vars_dataframe()
# model_out.head(5)

ax = model_out[["Quiescent","Active", "Jailed", "Fighting"]].plot()
ax.set_title('Citizen Condition Over Time')
ax.set_xlabel('Step')
ax.set_ylabel('Number of Citizens')
_ = ax.legend(bbox_to_anchor=(1.35, 1.025))
plt.tight_layout()
<<<<<<< HEAD
plt.savefig("figures_normalgrid/plot_"+legitimacy_kind+"_"+str(cop_density)+"_"+str(smart_cops)+".png")
=======
plt.savefig(r"C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block3\ABM\figures_normalgrid/plot_"+legitimacy_kind+"_"+str(cop_density)+"_"+str(smart_cops)+".png")
>>>>>>> 999953f52a88c79d3a33d0b48892d4544ca4c12b
plt.show()
if legitimacy_kind != "Local":
    ax = model_out[["Legitimacy"]].plot()
    ax.set_title('Citizen Condition Over Time')
    ax.set_xlabel('Step')
    ax.set_ylabel('Number of Citizens')
    _ = ax.legend(bbox_to_anchor=(1.35, 1.025))
    plt.tight_layout()
<<<<<<< HEAD
    plt.savefig("figures_normalgrid/legit_"+legitimacy_kind+"_"+str(cop_density)+"_"+str(smart_cops)+".png")
=======
    plt.savefig(r"C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block3\ABM\figures_normalgrid/legit_"+legitimacy_kind+"_"+str(cop_density)+"_"+str(smart_cops)+".png")
>>>>>>> 999953f52a88c79d3a33d0b48892d4544ca4c12b
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
<<<<<<< HEAD
    plt.savefig("figures_normalgrid/legit_"+legitimacy_kind+"_"+str(cop_density)+"_"+str(smart_cops)+".png")
=======
    plt.savefig(r"C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block3\ABM\figures_normalgrid/legit_"+legitimacy_kind+"_"+str(cop_density)+"_"+str(smart_cops)+".png")
>>>>>>> 999953f52a88c79d3a33d0b48892d4544ca4c12b
    plt.tight_layout()
    plt.show()

# single_agent_out = agent_out[single_agent]

# single_agent_out.head()
# 
