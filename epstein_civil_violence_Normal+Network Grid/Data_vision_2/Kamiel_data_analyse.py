#%%
import matplotlib.pyplot as plt
import importlib
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import seaborn as sns
from scipy import stats

legitimacy_kind = "Global"
frames = []
distribution = []
net = []
sum_actives = []
networks = ["Barabasi", "Renyi", "Small_world","None"]
n_sim = 400
time_peaks = []
peak_interval = []
for network in networks:
    for n in range(n_sim):
        # epstein_civil_violence_Normal+Network Grid\Data_vision_7\model_temp_Barabasi_Global_1.csv
       
        model_out = pd.read_csv(f"model_temp_{network}_{legitimacy_kind}_{n}.csv")
        actives = model_out["Active"]
        actives = np.array(actives)

        s_actives = sum(actives)
    
        f_peaks = find_peaks(actives, height=50, distance = 5)[1]
        f_peaks_time, _ = find_peaks(actives, height=50, distance = 5)

        # print(f_peaks_time)
        
        peaks = f_peaks["peak_heights"]
        mean_peaksize = np.mean(peaks)
        std_peaksize = np.std(peaks)
       
        net.append(network)
        sum_actives.append(s_actives)

    
        for i in range(len(f_peaks_time) - 1):
            peak_interval.append(f_peaks_time[i + 1] - f_peaks_time[i])
            
        mean_peak_interval  = np.mean(peak_interval)
        std_peak_interval = np.std(peak_interval)


            
        perc_reb = sum(active > 50 for active in actives)/len(actives)
        perc_calm = sum(active == 0 for active in actives)/len(actives)

        distribution.append([network,len(peaks), mean_peaksize,std_peaksize, mean_peak_interval, std_peak_interval, s_actives, perc_reb, perc_calm])
        if n > 0:
            model_out.drop([0])
        frames.append(model_out)

result = pd.concat(frames)
# plt.style.use('ggplot')
# x = "Total actives"
x = 'Peaks'
# x = 'Mean peak interval'
# x = "Mean peak size"

df = pd.DataFrame(distribution,columns=["Network", "Peaks","Mean peak size","Std peak size","Mean peak interval","std peak interval", "Total actives" ,"Percentage rebelious", "Percentage calm"])

df


analysis = df.loc[(df['Network'] == 'None')]
ax = sns.histplot(data=analysis, x=x, kde=True, bins=10)
ax.set_xlabel("Bin", size = 13)
ax.set_ylabel('Frequency', size = 13)
# ax.set_title(f"Distribution of {x} - None", size = 13)

# plt.savefig(f"Data_visualisation/data = {x} network = None.pdf")
plt.show()

analysis = df.loc[(df['Network'] == 'Barabasi')]

ax = sns.histplot(data=analysis, x=x, kde=True, bins=10)
ax.set_xlabel("Bin", size = 13)
ax.set_ylabel('Frequency', size = 13)
# ax.set_title(f"Distribution of {x} - Barabasi", size = 13)

# plt.savefig(f"Data_visualisation/data = {x} network = Barabsi.pdf")
plt.show()


analysis = df.loc[(df['Network'] == 'Renyi')]
ax = sns.histplot(data=analysis, x=x, kde=True, bins=10)

ax.set_xlabel("Bin", size = 13)
ax.set_ylabel('Frequency', size = 13)
# ax.set_title(f"Distribution of {x} - Renyi", size = 13)

# plt.savefig(f"Data_visualisation/data = {x} network = Renyi.pdf")
plt.show()

analysis = df.loc[(df['Network'] == 'Small-world')]
ax = sns.histplot(data=analysis, x=x, kde=True, bins=10)

ax.set_xlabel("Bin", size = 13)
ax.set_ylabel(x, size = 13)
# ax.set_title(f"Distribution of {x} - Small-world", size = 13)

# plt.savefig(f"Data_visualisation/data = {x} network = Small-world.pdf")
plt.show()




# sns.lineplot(data=result, x="Unnamed: 0", y="Active")
# sns.lineplot(data=result, x="Unnamed: 0", y="Fighting")
# sns.lineplot(data=result, x="Unnamed: 0", y="Quiescent") 

plt.show()

ax = sns.boxplot(x="Network", y=x, data=df)
# ax.set_title(f"Boxplot of {x}", size = 13)
ax.set_xlabel(" ", size = 13)
ax.set_ylabel('Frequency', size = 13)
# plt.savefig(f"Data_visualisation/data = {x}.pdf")


None_ = df.loc[(df['Network'] == 'None')]
Renyi = df.loc[(df['Network'] == 'Renyi')]
Barabasi = df.loc[(df['Network'] == 'Barabasi')]
Small_world = df.loc[(df['Network'] == 'Small_world')]


None_ = np.array(None_[x])
Renyi = np.array(Renyi[x])
Barabasi = np.array(Barabasi[x])
Small_world = np.array(Small_world[x])
plt.show()


None_ = np.nan_to_num(None_,np.nan)
Renyi = np.nan_to_num(Renyi,np.nan)
Barabasi =  np.nan_to_num(Barabasi,np.nan)
Small_world =  np.nan_to_num(Small_world,np.nan)



print("Shapiro None: ",stats.shapiro(None_))
print("Shapiro Renyi: ",stats.shapiro(Renyi))
print("Shapiro Barabasi: ",stats.shapiro(Barabasi))
print("Shapiro Small world: ",stats.shapiro(Small_world))

print("t-test None - Renyi", stats.ttest_ind(None_,Renyi))
print("t-test None - Barabasi", stats.ttest_ind(None_,Barabasi))
print("t-test None - Small world", stats.ttest_ind(None_,Small_world))
print("t-test Barabasi - Renyi", stats.ttest_ind(Barabasi,Renyi))
print("t-test Small world - Renyi", stats.ttest_ind(Small_world,Renyi))
print("t-test Barabasi - Small-world", stats.ttest_ind(Barabasi,Small_world))
 
# %%