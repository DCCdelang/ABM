import matplotlib.pyplot as plt
import importlib

from epstein_civil_violence.agent import Citizen, Cop
from epstein_civil_violence.model import EpsteinCivilViolence

import time

cop_density = .04
legitimacy = .82
smart_cops = True

start = time.time()
model = EpsteinCivilViolence(height=40, 
                           width=40, 
                           citizen_density=.7, 
                           cop_density=cop_density, 
                           citizen_vision=7, 
                           cop_vision=7, 
                           legitimacy=legitimacy, 
                           max_jail_term=30, 
                           max_iters=500,
                           smart_cops = smart_cops) # cap the number of steps the model takes
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
plt.savefig("figures/plot_"+str(cop_density)+"_"+str(smart_cops)+".png")
plt.show()

ax = model_out[["Legitimacy"]].plot()
ax.set_title('Citizen Condition Over Time')
ax.set_xlabel('Step')
ax.set_ylabel('Number of Citizens')
_ = ax.legend(bbox_to_anchor=(1.35, 1.025))
plt.tight_layout()
plt.savefig("figures/legit_"+str(cop_density)+"_"+str(smart_cops)+".png")
plt.show()