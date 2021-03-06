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
networks = ["Barabasi"]
n_sim = 400
time_peaks = []
peak_interval = []

plot = False
legitimacy = ["Fixed","Global","Local"]
vision = 7
for network in networks:

    
    if plot == True:
        model_out = pd.read_csv(f"/model_temp_{vision}_{network}_{legitimacy_kind}_0.csv")
        result = model_out
        # plt.figure(figsize=(15,8))
        ax = sns.lineplot(data=result, x="Unnamed: 0", y="Active", color="firebrick")
        ax.set_xlabel('Step', size = 13)
        ax.set_ylabel('Number of Active citizens', size = 13)
        ax.set_title(f'Active citizens Over Time - {network}', size = 13)
        plt.locator_params(axis='y', nbins=6)
        plt.locator_params(axis='x', nbins=5)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        
        plt.savefig(f"Actives_Single_sim_{network}.pdf")

        plt.show()
        # plt.figure(figsize=(15,8))
        ax = sns.lineplot(data=result, x="Unnamed: 0", y="Legitimacy", color="dodgerblue")
        ax.set_xlabel('Step', size = 13)
        ax.set_ylabel('Legitemacy', size = 13)
        ax.set_title(f'Citizen Condition Over Time - {network}', size = 13)
        plt.locator_params(axis='y', nbins=6)
        plt.locator_params(axis='x', nbins=5)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        
        plt.savefig(f"Legitimacy_Single_sim_{network}.pdf")
        plt.show()
    
    else:
        for legitimacy_kind in legitimacy:
            for n in range(n_sim):
                if legitimacy_kind == "Global":
                    model_out = pd.read_csv(f"model_temp_{network}_{legitimacy_kind}_{n}.csv")
                else:
                    model_out = pd.read_csv(f"model_temp_{vision}_{network}_{legitimacy_kind}_{n}.csv")
                # epstein_civil_violence_Normal+Network Grid\Data_vision_7\model_temp_Barabasi_Global_1.csv
                
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

                distribution.append([network,len(peaks), mean_peaksize,std_peaksize, mean_peak_interval, std_peak_interval, s_actives, perc_reb, perc_calm, legitimacy_kind])
                if n > 0:
                    model_out.drop([0])
                frames.append(model_out)

result = pd.concat(frames)
# plt.style.use('ggplot')
x = "Total actives"
# x = 'Peaks'
# x = 'Mean peak interval'
# x = "Mean peak size"

x_s = ["Total actives", "Peaks", "Mean peak interval", "Mean peak size"]
df = pd.DataFrame(distribution,columns=["Network", "Peaks","Mean peak size","Std peak size","Mean peak interval","std peak interval", "Total actives" ,"Percentage rebelious", "Percentage calm", "Legitimacy"])

print(df)


# analysis = df.loc[(df['Network'] == 'None')]
# ax = sns.histplot(data=analysis, x=x, kde=True, bins=10)
# ax.set_xlabel("Bin", size = 13)
# ax.set_ylabel('Frequency', size = 13)
# # ax.set_title(f"Distribution of {x} - None", size = 13)

# plt.savefig(f"Data_visualisation/data = {x} network = None.pdf")
# plt.show()

# analysis = df.loc[(df['Network'] == 'Barabasi')]

# ax = sns.histplot(data=analysis, x=x, kde=True, bins=10)
# ax.set_xlabel("Bin", size = 13)
# ax.set_ylabel('Frequency', size = 13)
# # ax.set_title(f"Distribution of {x} - Barabasi", size = 13)

# plt.savefig(f"Data_visualisation/data = {x} network = Barabsi.pdf")
# plt.show()


# analysis = df.loc[(df['Network'] == 'Renyi')]
# ax = sns.histplot(data=analysis, x=x, kde=True, bins=10)

# ax.set_xlabel("Bin", size = 13)
# ax.set_ylabel('Frequency', size = 13)
# # ax.set_title(f"Distribution of {x} - Renyi", size = 13)

# plt.savefig(f"Data_visualisation/data = {x} network = Renyi.pdf")
# plt.show()

# analysis = df.loc[(df['Network'] == 'Small-world')]
# ax = sns.histplot(data=analysis, x=x, kde=True, bins=10)

# ax.set_xlabel("Bin", size = 13)
# ax.set_ylabel(x, size = 13)
# # ax.set_title(f"Distribution of {x} - Small-world", size = 13)

# plt.savefig(f"Data_visualisation/data = {x} network = Small-world.pdf")
# plt.show()





for x in x_s:
    Global = df.loc[(df["Legitimacy"] == 'Global')]
    Local = df.loc[(df["Legitimacy"] == 'Local')]
    Fixed = df.loc[(df["Legitimacy"] == 'Fixed')]
    print(x)
    print("\n")
    ax = sns.violinplot(x="Legitimacy", y=x, data=df)

    # ax.set_title(f"Boxplot of {x}", size = 13)
    ax.set_xlabel(" ", size = 14)
    plt.locator_params(nbins=4)
    plt.ylabel("Frequency", fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()
    plt.savefig(f"Legitimacy_data = {x}.pdf")
    plt.show()

    # None_ = df.loc[(df['Network'] == 'None')]
    # Renyi = df.loc[(df['Network'] == 'Renyi')]
    # Barabasi = df.loc[(df['Network'] == 'Barabasi')]
    # Small_world = df.loc[(df['Network'] == 'Small-world')]


    # None_ = np.array(None_[x])
    # Renyi = np.array(Renyi[x])
    # Barabasi = np.array(Barabasi[x])
    # Small_world = np.array(Small_world[x])
    # plt.show()


    # None_ = np.nan_to_num(None_,np.nan)
    # Renyi = np.nan_to_num(Renyi,np.nan)
    # Barabasi =  np.nan_to_num(Barabasi,np.nan)
    # Small_world =  np.nan_to_num(Small_world,np.nan)

    Fixed = np.array(Fixed[x])
    Local = np.array(Local[x])
    Global = np.array(Global[x])

    Fixed = np.nan_to_num(Fixed,np.nan)
    Local = np.nan_to_num(Local,np.nan)
    Global =  np.nan_to_num(Global,np.nan)

    # print("Shapiro None: ",stats.shapiro(None_))
    # print("Shapiro Renyi: ",stats.shapiro(Renyi))
    # print("Shapiro Barabasi: ",stats.shapiro(Barabasi))
    # print("Shapiro Small world: ",stats.shapiro(Small_world))

    print("Mean fixed", np.mean(Fixed))
    print("Mean local", np.mean(Local))
    print("Mean Globasl", np.mean(Global))
    print("t-test Fixed - Global", stats.ttest_ind(Fixed,Global))
    print("t-test Fixed - Local", stats.ttest_ind(Fixed,Local))
    print("t-test Local - Global", stats.ttest_ind(Local,Global))


    # print("t-test None - Renyi", stats.ttest_ind(None_,Renyi))
    # print("t-test None - Barabasi", stats.ttest_ind(None_,Barabasi))
    # print("t-test None - Small world", stats.ttest_ind(None_,Small_world))
    # print("t-test Barabasi - Renyi", stats.ttest_ind(Barabasi,Renyi))
    # print("t-test Small world - Renyi", stats.ttest_ind(Small_world,Renyi))
    # print("t-test Barabasi - Small-world", stats.ttest_ind(Barabasi,Small_world))
 
# %%
