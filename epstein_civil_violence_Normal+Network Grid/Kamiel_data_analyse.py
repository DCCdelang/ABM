#%%
import matplotlib.pyplot as plt
import importlib
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import seaborn as sns

legitimacy_kind = "Fixed"
frames = []
distribution = []
net = []
sum_actives = []
networks = ["Barabasi", "Renyi", "Small-world"]
n_sim = 300
for network in networks:
    for n in range(n_sim):
        model_out = pd.read_csv(f"epstein_civil_violence_Normal+Network Grid/Data/model_temp_{network}_{legitimacy_kind}_{n}.csv")
        actives = model_out["Active"]
        actives = np.array(actives)

        s_actives = sum(actives)
    
        f_peaks = find_peaks(actives, height=50)[1]

        peaks = f_peaks["peak_heights"]

        distribution.append([network,len(peaks), s_actives])
        net.append(network)
        sum_actives.append(s_actives)

        if n > 0:
            model_out.drop([0])
        frames.append(model_out)

result = pd.concat(frames)

x = "Tot_actives"
x = 'Peaks'
print(distribution)

df = pd.DataFrame(distribution,columns=["Network", "Peaks", "Tot_actives"])

analysis = df.loc[(df['Network'] == 'Barabasi')]

sns.histplot(data=analysis, x=x, kde=True)
plt.show()


analysis = df.loc[(df['Network'] == 'Renyi')]

sns.histplot(data=analysis, x=x, kde=True)
plt.show()

analysis = df.loc[(df['Network'] == 'Small-world')]

sns.histplot(data=analysis, x=x, kde=True)
plt.show()




# sns.lineplot(data=result, x="Unnamed: 0", y="Active")
# sns.lineplot(data=result, x="Unnamed: 0", y="Fighting")
# sns.lineplot(data=result, x="Unnamed: 0", y="Quiescent")

plt.show()


# %%
