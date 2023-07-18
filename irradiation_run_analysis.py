import numpy as np
import matplotlib.pyplot as plt
import math
from functions import *
from read_from_file import *
from ohm_run_variables import *

plt.xlabel('time (s)')
plt.ylabel('Voltage (mV)')
plt.rcParams["figure.figsize"] = [20, 15]


generator = read_irr_file() # Variable are read from read_from_file.py
time_pre = int(next(generator))
time_dis = int(next(generator))
time_post = int(next(generator))
total_time = time_pre + time_dis + time_post
T_cal= next(generator)
R_burster= next(generator)
tme = next(generator)
voltages = next(generator)
plt.plot(tme, voltages, c = 'red')
plt.show()
plt.close()


plt.plot(tme[1:time_pre - 4], voltages[1:time_pre - 4], c='blue') # pre-drift is plotted in blue
plt.plot(tme[time_pre + time_dis + 5:total_time + 1],voltages[time_pre + time_dis + 5:total_time + 1], c='red') # pre-drift is plotted in red
plt.show()
plt.close()
def ohm_calibration(time_pre_ohm, time_ohm, time_post_ohm, total_time_ohm, tme_ohm, voltages_ohm):
    a, b = np.polyfit(tme_ohm[1:time_pre_ohm - 4],voltages_ohm[1:time_pre_ohm - 4], 1) # Line of best fit of pre-drift
    pre_volt = a * (total_time_ohm - time_ohm - time_post_ohm + 0.5 * time_ohm) + b # Forward extrapolated to determine value at midpoint
  
    a, b = np.polyfit(tme_ohm[time_pre_ohm + 5 :total_time_ohm - time_post_ohm - 4],voltages_ohm[time_pre_ohm + 5:total_time_ohm - time_post_ohm - 4], 1)
    top_volt = a * (total_time_ohm - time_ohm - time_post_ohm + 0.5 * time_ohm) + b

    a, b = np.polyfit(tme_ohm[time_pre_ohm + time_ohm + 5:total_time_ohm + 1],voltages_ohm[time_pre_ohm + time_ohm + 5:total_time_ohm + 1], 1)
    post_volt = a * (total_time_ohm - time_ohm - time_post_ohm + 0.5 * time_ohm) + b

    calibration = (((top_volt - pre_volt) + (top_volt - post_volt))/2)*1e-3 # The average between the two delta_V
    
    return calibration # returns (deltaV/deltaR)_1ohm

def deltaV_to_deltaT(time_pre, time_dis, time_post, total_time, tme, voltages, T_cal, R_burster):
    a, b = np.polyfit(tme[1:time_pre - 4],voltages[1:time_pre - 4], 1)
    pre_volt = a * (total_time - time_dis - time_post + 0.5 * time_dis) + b 
       
    a, b = np.polyfit(tme[time_pre + time_dis + 5:total_time +1],voltages[time_pre + time_dis + 5:total_time +1], 1)
    post_volt = a * (total_time - time_dis - time_post + 0.5 * time_dis) + b
    
    delta_volt = (post_volt - pre_volt)*1e-3 # deltaV (V)

     
    #inst = access_multimeter() # # Communication with multimeter to read four series resistance for use in T_cal calculation function is imported from functions.py
    
    #inst.write("ROUTe:CLOSe (@1)") # # The below is not needed as T_cal is read from the irradiation run text file
    #inst.write("ROUTe:OPEN (@1)")
    # R_temp = float(inst.query(':MEASure:FRESistance?'))
    # R_temp = 114
    # temp_probe = 1 # # The below constants are based on which RTD probe is used
    
    # if int(temp_probe) == 1:
    #     AI = 0.003942247616179
    #     BI = -2.06E-06
    #     RI = 99.87328
    # elif int(temp_probe) == 2:
    #     AI = 0.003931584
    #     BI = -1.8364E-06
    #     RI = 99.937458
    # elif int(temp_probe) == 3:
    #     AI = 0.00385991
    #     BI = -1.089E-06
    #     RI = 100.039338
    # elif int(temp_probe) == 4:
    #     AI = 3.86763e-3
    #     BI = 4.73227e-6
    #     RI = 100.04722
    # else:
    #     AI = 3.89020e-3
    #     BI = 2.09532e-6
    #     RI = 100.04198
    
    #T_cal = (-1*AI+(math.sqrt((AI*AI)-(4*BI*(1-(R_temp/RI))))))/(2*BI)
    beta = 3112.621146
    deltaV_deltaR = ohm_calibration(time_pre_ohm, time_ohm, time_post_ohm, total_time_ohm, tme_ohm, voltages_ohm)
    #deltaV_deltaR = 25e-6
    delta_T = (delta_volt*T_cal**2)/(deltaV_deltaR*R_burster*beta)
    
    return delta_T

print(deltaV_to_deltaT(time_pre, time_dis, time_post, total_time, tme, voltages, T_cal, R_burster))
