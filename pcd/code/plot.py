# -*- coding: utf-8 -*-
"""
Created on Thu May  3 03:42:00 2018

@author: fakher
"""
import matplotlib.pyplot as plt
from pt import *

plt.close('all')
detector = QRSDetectorOffline(ecg_data_path="..\\code\\data\\100.csv", verbose=False,
                                      log_data=False, plot_data=False, show_plot=False)


raw_ecg = detector.ecg_data_raw[:540, 1]
q = [detector.detected_peaks_indices, detector.detected_peaks_values] 


fig, ax = plt.subplots(1, 1)
ax.plot(raw_ecg)
#ax.scatter(q[0], q[1], c="yellow", s=50, zorder=2)
#ax.scatter(r[0], r[1], c="black", s=50, zorder=2)
#ax.scatter(s[0], s[1], c="red", s=50, zorder=2)
plt.show()
plt.close('all')