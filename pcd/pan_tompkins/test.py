# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 04:52:03 2018

@author: fakher
"""
import numpy as np
import matplotlib.pyplot as plt 
from neurokit import ecg_process
import _extract_data
import pt

def extract(name):
    rate, sampwidth, data = _extract_data.readwav(name)
    return rate, sampwidth, data

r, s, data = extract('./data/sig100.wav')
data = data[:,0]

data = data[:2000]
features = ecg_process(data, sampling_rate=360)['ECG']

plt.plot(data)
plt.scatter(features['R_Peaks'], np.ones(len(features['R_Peaks'])) * max(data), s=50, c='black')
plt.show()

qrs_detector = pt.QRSDetectorOffline(ecg_data_path="./data/sig100.wav", verbose=False,
                                      log_data=False, plot_data=False, show_plot=False)