# This python file extracts the ohm run values from the read_ohm_file

import numpy as np
import matplotlib.pyplot as plt
from read_from_file import * # All functions and variables are imported from read_from_file.py

plt.xlabel('Time (s)')
plt.ylabel('Voltages (mK)')
plt.rcParams["figure.figsize"] = [20, 15]

generator = read_ohm_file() # read_ohm_file() becomes a generator object
time_pre_ohm = int(next(generator)) # First yield result is given to variable time_pre_ohm
time_ohm = int(next(generator))
time_post_ohm = int(next(generator))
total_time_ohm = time_pre_ohm + time_ohm + time_post_ohm
next(generator) # The temperature of the water and burster setting is ignored as it isn't used in any calculations (Extracted from text file just in case)
next(generator)
tme_ohm = next(generator)
voltages_ohm = next(generator)
plt.plot(tme_ohm, voltages_ohm, c = 'red') # All time and voltage data points are plotted
plt.show()


plt.plot(tme_ohm[1:time_pre_ohm - 4],voltages_ohm[1:time_pre_ohm - 4], c='blue') # Pre-drift is plotted in blue 
plt.plot(tme_ohm[time_pre_ohm + 5:total_time_ohm - time_post_ohm - 4],voltages_ohm[time_pre_ohm + 5:total_time_ohm - time_post_ohm - 4], c='black') # Duration of 1 ohm gain is plotted in black
plt.plot(tme_ohm[time_pre_ohm + time_ohm + 5:total_time_ohm + 1],voltages_ohm[time_pre_ohm + time_ohm + 5:total_time_ohm +1], c='red') # Post-drift is plotted in red
plt.show()
plt.close()

