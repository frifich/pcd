import numpy as np
import matplotlib.pyplot as plt
from pantompkins import *

my_data = np.loadtxt('./my_ecg.csv', skiprows=1, delimiter=',')
my_data = my_data[:1000, 1]
plt.plot(my_data)
my_qrs = run(my_data)
plt.scatter(my_qrs, my_data[my_qrs])
plt.show()
