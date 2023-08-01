import numpy as np
import matplotlib.pyplot as plt
from functions import *
from read_from_file import *
# from live_ohm_run import * # # Keep these comments commented unless connected to device
# from live_irr_run import *
# from T_cal_calc import *

plt.xlabel('time (s)')
plt.ylabel('Voltage (mV)')
plt.rcParams["figure.figsize"] = [20, 15]



R_burster = 19669
pre_drift_ignore = 5
post_drift_ignore = 5
ohm_run_ignore = 2


# # Irradiation run variables are read from read_from_file.py
generator = read_irr_file()
time_pre = int(next(generator))
time_dis = int(next(generator))
time_post = int(next(generator))
total_time = time_pre + time_dis + time_post
T_cal = next(generator)
R_burster = next(generator)
tme = next(generator)
voltages = next(generator)


plt.plot(tme, voltages)
plt.show()
plt.close()
    

plt.xlabel('time (s)')
plt.ylabel('Voltage (mV)')
plt.rcParams["figure.figsize"] = [20, 15]
plt.plot(tme[1:time_pre - pre_drift_ignore + 1], voltages[1:time_pre - pre_drift_ignore + 1], c='blue') # pre-drift is plotted in blue
plt.plot(tme[time_pre + time_dis + post_drift_ignore:total_time + 1],voltages[time_pre + time_dis + post_drift_ignore:total_time + 1], c='red') # post-drift is plotted in red
plt.show()
plt.close()


# # Ohm run variables are read from read_from_file.py, otherwise it is taken from live_ohm_run.py
generator = read_ohm_file() # read_ohm_file() becomes a generator object
time_pre_ohm = int(next(generator)) # First yield result is given to variable time_pre_ohm
time_ohm = int(next(generator))
time_post_ohm = int(next(generator))
total_time_ohm = time_pre_ohm + time_ohm + time_post_ohm
tme_ohm = next(generator)
voltages_ohm = next(generator)

    
    
    
plt.xlabel('time (s)')
plt.ylabel('Voltage (mV)')
plt.rcParams["figure.figsize"] = [20, 15]
plt.plot(tme_ohm, voltages_ohm) # All time and voltage data points are plotted
plt.show()
    

plt.xlabel('time (s)')
plt.ylabel('Voltage (mV)')
plt.rcParams["figure.figsize"] = [20, 15]
plt.plot(tme_ohm[1:time_pre_ohm - 4],voltages_ohm[1:time_pre_ohm - 4], c='blue') # Pre-drift is plotted in blue 
plt.plot(tme_ohm[time_pre_ohm + 5:total_time_ohm - time_post_ohm - 4],voltages_ohm[time_pre_ohm + 5:total_time_ohm - time_post_ohm - 4], c='black') # Duration of 1 ohm gain is plotted in black
plt.plot(tme_ohm[time_pre_ohm + time_ohm + 5:total_time_ohm + 1],voltages_ohm[time_pre_ohm + time_ohm + 5:total_time_ohm +1], c='red') # Post-drift is plotted in red
plt.show()
plt.close()


def ohm_calibration(time_pre_ohm, time_ohm, time_post_ohm, total_time_ohm, tme_ohm, voltages_ohm, pre_drift_ignore, post_drift_ignore, ohm_run_ignore):
    a, b = np.polyfit(tme_ohm[1:time_pre_ohm - pre_drift_ignore + 1],voltages_ohm[1:time_pre_ohm - pre_drift_ignore + 1], 1) # Line of best fit of pre-drift
    pre_volt = a * (total_time_ohm - time_ohm - time_post_ohm + 0.5 * time_ohm) + b # Forward extrapolated to determine value at midpoint
  
    a, b = np.polyfit(tme_ohm[time_pre_ohm + ohm_run_ignore :total_time_ohm - time_post_ohm - ohm_run_ignore + 1], voltages_ohm[time_pre_ohm + ohm_run_ignore:total_time_ohm - time_post_ohm - ohm_run_ignore + 1], 1)
    top_volt = a * (total_time_ohm - time_ohm - time_post_ohm + 0.5 * time_ohm) + b

    a, b = np.polyfit(tme_ohm[time_pre_ohm + time_ohm + post_drift_ignore:total_time_ohm + 1],voltages_ohm[time_pre_ohm + time_ohm + post_drift_ignore:total_time_ohm + 1], 1)
    post_volt = a * (total_time_ohm - time_ohm - time_post_ohm + 0.5 * time_ohm) + b

    calibration = (((top_volt - pre_volt) + (top_volt - post_volt))/2)*1e-3 # The average between the two delta_V
    
    return calibration # returns (deltaV/deltaR)_1ohm

def deltaV_to_deltaT(time_pre, time_dis, time_post, total_time, tme, voltages, R_burster, pre_drift_ignore, post_drift_ignore, T_cal):
    a, b = np.polyfit(tme[1:time_pre - pre_drift_ignore + 1],voltages[1:time_pre - pre_drift_ignore + 1], 1)
    pre_volt = a * (total_time - time_dis - time_post + 0.5 * time_dis) + b 
       
    a, b = np.polyfit(tme[time_pre + time_dis + post_drift_ignore:total_time +1],voltages[time_pre + time_dis + post_drift_ignore:total_time +1], 1)
    post_volt = a * (total_time - time_dis - time_post + 0.5 * time_dis) + b
    
    delta_volt = (post_volt - pre_volt)*1e-3 # deltaV (V)
        
    beta = 3112.621146 # Beta value of one of the two probes
    deltaV_deltaR = ohm_calibration(time_pre_ohm, time_ohm, time_post_ohm, total_time_ohm, tme_ohm, voltages_ohm, pre_drift_ignore, post_drift_ignore, ohm_run_ignore)
    #deltaV_deltaR = 25e-6 # # The above should be approximately equal to this value
    delta_T = (delta_volt*T_cal**2)/(deltaV_deltaR*R_burster*beta)
    
    return delta_T

print(deltaV_to_deltaT(time_pre, time_dis, time_post, total_time, tme, voltages, R_burster, pre_drift_ignore, post_drift_ignore, T_cal), "K")
