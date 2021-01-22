import matplotlib.pyplot as plt
import importlib

from epstein_civil_violence.agent import Citizen, Cop
from epstein_civil_violence.model import EpsteinCivilViolence

import time

cop_density = .074
legitimacy = .82
smart_cops = False

start = time.time()
model = EpsteinCivilViolence(n_nodes=1000, 
                           links=112, 
                           citizen_density=.7, 
                           cop_density=0.04, 
                           citizen_vision=7, 
                           cop_vision=7, 
                           legitimacy=legitimacy, 
                           max_jail_term=30, 
                           max_iters=500, # cap the number of steps the model takes
                           smart_cops = False,
                           max_fighting_time = 1,
                           network= "barbasi_albert") # Choose the kind of network: barbasi_albert, watts_strogatz, erdos_renyi
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
#plt.savefig("figures_networkgrid/plot_"+str(cop_density)+"_"+str(smart_cops)+".png")
plt.show()

ax = model_out[["Legitimacy"]].plot()
ax.set_title('Citizen Condition Over Time')
ax.set_xlabel('Step')
ax.set_ylabel('Number of Citizens')
_ = ax.legend(bbox_to_anchor=(1.35, 1.025))
plt.tight_layout()
#plt.savefig("figures_networkgrid/legit_"+str(cop_density)+"_"+str(smart_cops)+".png")
plt.show()