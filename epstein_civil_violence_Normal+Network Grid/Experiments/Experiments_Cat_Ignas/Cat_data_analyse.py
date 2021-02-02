#%%
import matplotlib.pyplot as plt
import importlib
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import seaborn as sns
import random


frames = []
distribution = []
net = []
sum_actives = []
networks = ["Barabasi", "Renyi", "SmallWorld", "None"]
n_sim = 5
"""
for network in networks:
    for n in range(n_sim):
        
        model_out = pd.read_csv(f"Network_result/Res - network({network}) - run({n}).csv")
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

sns.boxplot(x=df['Network'], y=df['Peaks'])
plt.show()


sns.boxplot(x=df['Network'], y=df['Tot_actives'])
plt.show()

analysis = df.loc[(df['Network'] == 'Barabasi')]

sns.histplot(data=analysis, x=x, kde=True)
plt.show()


analysis = df.loc[(df['Network'] == 'Renyi')]

sns.histplot(data=analysis, x=x, kde=True)
plt.show()

analysis = df.loc[(df['Network'] == 'SmallWorld')]

sns.histplot(data=analysis, x=x, kde=True)
plt.show()

analysis = df.loc[(df['Network'] == 'None')]

sns.histplot(data=analysis, x=x, kde=True)
plt.show()
"""
"""
#networks = ["Barabasi"]
for network in networks:
    frames = []
    for n in range(n_sim):
        
        model_out = pd.read_csv(f"Network_result/Res - network({network}) - run({n}).csv")
        frames.append(model_out)
    result = pd.concat(frames)
    #print(result)
    ax = sns.lineplot(data=result, x="Unnamed: 0", y="Active", label="Active")
    sns.lineplot(data=result, x="Unnamed: 0", y="Fighting", label="Fighting")
    sns.lineplot(data=result, x="Unnamed: 0", y="Quiescent", label="Quiescent")
    sns.lineplot(data=result, x="Unnamed: 0", y="Jailed", label="Jailed")
    ax.set_xlabel('Step')
    ax.set_ylabel('Number of Citizens')
    ax.set_title(f'Citizen Condition Over Time - {network}')

    plt.legend()
    plt.show()
    
"""

#networks = ["Barabasi"]
pal = ["forestgreen", "firebrick", "darkorange", "mediumorchid"]
pal = [ "green", "red", "blue","orange"]
#sns.set(rc={'figure.figsize':(15,8)})
for network in networks:
    frames = []
    for n in range(n_sim):
        
        model_out = pd.read_csv(f"Network_result/Res - network({network}) - run({n}).csv")
        
    #print(result)
        if n == 0:
            ax = sns.lineplot(data=model_out, x="Unnamed: 0", y="Active", label="Active", color = pal[1], linewidth=0.8)
            sns.lineplot(data=model_out, x="Unnamed: 0", y="Fighting", label="Fighting", color = pal[2], linewidth=0.8)
            sns.lineplot(data=model_out, x="Unnamed: 0", y="Quiescent", label="Quiescent", color = pal[3], linewidth=0.8)
            sns.lineplot(data=model_out, x="Unnamed: 0", y="Jailed", label="Jailed", color = pal[0], linewidth=0.8)
            ax.set_xlabel('Step', size=17)
            ax.set_ylabel('Number of Citizens', size = 17)
            ax.set_title(f'Citizen Condition Over Time - {network}', size = 20)
        else:
            ax = sns.lineplot(data=model_out, x="Unnamed: 0", y="Active", color = pal[1], linewidth=0.8)
            sns.lineplot(data=model_out, x="Unnamed: 0", y="Fighting", color = pal[2], linewidth=0.8)
            sns.lineplot(data=model_out, x="Unnamed: 0", y="Quiescent", color = pal[3], linewidth=0.8)
            sns.lineplot(data=model_out, x="Unnamed: 0", y="Jailed", color = pal[0], linewidth=0.8)           
    #plt.figure(figsize=(8,15))        
    
    plt.savefig(f"Long_run_figures/All_sim_{network}.pdf")
    plt.show()
"""
pal = ["forestgreen", "firebrick", "darkorange", "mediumorchid"]
for network in networks:
    frames = []
    n = random.randrange(5)
        
    model_out = pd.read_csv(f"Network_result/Res - network({network}) - run({n}).csv")
        
    #print(result)
    ax = sns.lineplot(data=model_out, x="Unnamed: 0", y="Active", label="Active", color = pal[1])
    sns.lineplot(data=model_out, x="Unnamed: 0", y="Fighting", label="Fighting", color = pal[2])
    sns.lineplot(data=model_out, x="Unnamed: 0", y="Quiescent", label="Quiescent", color = pal[3])
    sns.lineplot(data=model_out, x="Unnamed: 0", y="Jailed", label="Jailed", color = pal[0])
    ax.set_xlabel('Step', size = 13)
    ax.set_ylabel('Number of Citizens', size = 13)
    ax.set_title(f'Citizen Condition Over Time - {network}', size = 13)
           
    #plt.figure(figsize=(8,15))        
    
    plt.savefig(f"Long_run_figures/Single_sim_{network}.pdf")
    plt.show()
"""
# %%
