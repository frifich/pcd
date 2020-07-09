# -*- coding: utf-8 -*-
"""
Created on Thu May  3 03:42:00 2018

@author: fakher
"""
import matplotlib.pyplot as plt
import numpy as np 
plt.close('all')

fig, ax = plt.subplots(1, 1)
raw100 = np.loadtxt('100.csv', skiprows=1, delimiter=',')
ax.plot(raw_ecg)
#ax.scatter(q[0], q[1], c="yellow", s=30, zorder=2)
#ax.scatter(r[0], r[1], c="black", s=50, zorder=2)
#ax.scatter(s[0], s[1], c="red", s=50, zorder=2)
plt.show()
plt.close('all')