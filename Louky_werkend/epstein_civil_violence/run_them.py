# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 12:23:46 2021

@author: Gebruiker
"""

import matplotlib.pyplot as plt

from epstein_civil_violence.agent import Citizen, Cop
from epstein_civil_violence.model import EpsteinCivilViolence

model = EpsteinCivilViolence(height=40, 
                           width=40, 
                           citizen_density=.7, 
                           cop_density=.04, 
                           citizen_vision=7, 
                           cop_vision=7, 
                           legitimacy=.82, 
                           max_jail_term=30, 
                           active_threshold=0.1,
                           arrest_prob_constant=2.3,
                       
                           max_iters=1000) # cap the number of steps the model takes
model.run_model()

model_out = model.datacollector.get_model_vars_dataframe()

ax = model_out.plot()
ax.set_title('Citizen Condition Over Time')
ax.set_xlabel('Step')
ax.set_ylabel('Number of Citizens')
_ = ax.legend(bbox_to_anchor=(1.35, 1.025))

plt.show()