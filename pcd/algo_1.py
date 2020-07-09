# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 04:45:44 2018

@author: fakher
"""
import matplotlib.pyplot as plt 
import numpy as np
import extract_data
import filters

#getting raw ecg
number_samples = 200
T = 15.0 # window
n = int(number_samples) # number of samples
t = np.linspace(0, T, n, endpoint=False)

rate, sampwidth, data = extract_data.extract('sig100.wav')
raw_ecg = data[:number_samples]
raw_ecg = raw_ecg[:, [0]]

#filtering
order = 10
fs = rate #sampling frequency
cutoff = 150 #cutoff frequency 
filtered_ecg = filters.butter_lowpass_filter(raw_ecg, cutoff, fs, order)

#plotting
plt.plot(t, raw_ecg, 'b-', label='raw_ecg')
plt.plot(t, filtered_ecg, 'r-', label='filtere_ecg')
plt.grid()
plt.legend()
plt.show()
    