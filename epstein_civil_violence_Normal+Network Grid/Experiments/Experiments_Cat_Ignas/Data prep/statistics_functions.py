import pandas as pd
import os
import numpy as np
from scipy.signal import find_peaks

def read_files_dir(path):
  '''function for reading and combining files in a directory'''
  os.chdir(path)
  file_list = os.listdir()
  df_1 = pd.DataFrame()
  for i in file_list:
    if i[len(i)-3:len(i)] != "csv":
      continue
    print(i)
    data = pd.read_csv(i)
    data["file"] = i
    df_1 = pd.concat([df_1, data])
  return df_1

def count_peaks(model):
    model_out = model
    peaks, _ = find_peaks(model_out["Active"], height=50, distance = 5)
    # print("Indices of peaks:", peaks, "Amount:", len(peaks))
    return len(peaks)
    
def mean_peak_size(model):
    model_out = model
    peaks, _ = find_peaks(model_out["Active"], height=50, distance = 5)
    actives_list = model_out["Active"].to_list()
    peak_sizes = []
    for peak in peaks:
        peak_sizes.append(actives_list[peak])
    return np.mean(peak_sizes)

def std_peak_size(model):
    model_out = model
    peaks, _ = find_peaks(model_out["Active"], height=50, distance = 5)
    actives_list = model_out["Active"].to_list()
    peak_sizes = []
    for peak in peaks:
        peak_sizes.append(actives_list[peak])
    return np.std(peak_sizes)

def mean_peak_interval(model):
    model_out = model
    peaks, _ = find_peaks(model_out["Active"], height=50, distance = 5)
    peak_intervals = []
    if len(peaks)>1:
        for i in range(len(peaks)-1):
            peak_intervals.append(peaks[i+1] - peaks[i])
    return np.mean(peak_intervals)

def std_peak_interval(model):
    model_out = model
    peaks, _ = find_peaks(model_out["Active"], height=50, distance = 5)
    peak_intervals = []
    if len(peaks)>1:
        for i in range(len(peaks)-1):
            peak_intervals.append(peaks[i+1] - peaks[i])
    return np.std(peak_intervals)

def perc_time_rebel(model):
    model_out = model
    actives_list = model_out["Active"].to_list()
    return sum(actives > 50 for actives in actives_list)/len(actives_list)

def perc_time_calm(model):
    model_out = model
    actives_list = model_out["Active"].to_list()
    return sum(actives == 0 for actives in actives_list)/len(actives_list)


def process_data(data):
    peaks = count_peaks(data)
    mean_peak_height = mean_peak_size(data)
    std_peak_height = std_peak_size(data)
    mean_peak_int = mean_peak_interval(data)
    std_peak_int = std_peak_interval(data)
    frac_time_rebelling = perc_time_rebel(data)
    frac_time_in_peace = perc_time_calm(data)
    run = data["run"][0]
    
    col_names = data.columns
    distinct_column_name = str(col_names[6])
    
    value = data[distinct_column_name][0]
    
    df_dict = {
        "mean_peak_size": [mean_peak_height],
        "std_peak_size": [std_peak_height],
        "mean_peak_interval": [mean_peak_int],
        "std_peak_interval": [std_peak_int],
        "frac_time_rebel": [frac_time_rebelling],
        "frac_time_calm": [frac_time_in_peace],
        "peaks": [peaks],
        distinct_column_name: [value],
        "run": [run]
        }
    
    return pd.DataFrame(df_dict)
    
    
def give_stats_file(path):
    os.chdir(path)
    file_list = os.listdir()
    df_stats_full = pd.DataFrame()
    for i in file_list:
        if i[len(i)-3:len(i)] != "csv":
            continue
        print(i)
        data = pd.read_csv(i)
        data_stats = process_data(data)
        df_stats_full = pd.concat([df_stats_full, data_stats])
    return df_stats_full
    

