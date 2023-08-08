import numpy as np
import matplotlib.pyplot as plt
from functions import *
from read_from_file import *
from ohm_run_analysis import *
import os
import csv

plt.xlabel('time (s)')
plt.ylabel('Voltage (mV)')
plt.rcParams["figure.figsize"] = [20, 15]

R_burster = 19669
pre_drift_ignore = 5
post_drift_ignore = 5


# # Irradiation run variables are read from read_from_file.py
generator = read_irr_file()
date_measure_irr = next(generator)
time_measure_irr = next(generator)
time_pre = int(next(generator))
time_dis = int(next(generator))
time_post = int(next(generator))
total_time = time_pre + time_dis + time_post
T_cal = next(generator)
R_burster = next(generator)
tme = next(generator)
voltages = next(generator)
# print(time_pre, time_dis, time_post, total_time, T_cal, R_burster, tme, voltages)



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


def deltaV(time_pre, time_dis, time_post, total_time, tme, voltages, R_burster, pre_drift_ignore, post_drift_ignore, T_cal):
    a, b = np.polyfit(tme[1:time_pre - pre_drift_ignore + 1],voltages[1:time_pre - pre_drift_ignore + 1], 1)
    pre_volt = a * (total_time - time_dis - time_post + 0.5 * time_dis) + b 
       
    a, b = np.polyfit(tme[time_pre + time_dis + post_drift_ignore:total_time +1],voltages[time_pre + time_dis + post_drift_ignore:total_time +1], 1)
    post_volt = a * (total_time - time_dis - time_post + 0.5 * time_dis) + b
    
    delta_volt = (post_volt - pre_volt)*1e-3 # deltaV (V)
    return delta_volt

def deltaV_to_deltaT(delta_volt, T_cal, R_burster):
    beta = 3112.621146 # Beta value of one of the two probes
    deltaV_deltaR = ohm_calibration(time_pre_ohm, time_ohm, time_post_ohm, total_time_ohm, tme_ohm, voltages_ohm, pre_drift_ignore, post_drift_ignore, ohm_run_ignore)
    #deltaV_deltaR = 25e-6 # # The above should be approximately equal to this value (V/ohm)
    delta_T = (delta_volt*T_cal**2)/(deltaV_deltaR*R_burster*beta)
    
    return delta_T

# File location where irr run analysis result is saved is extracted below
filename = "irr_analysis_results.csv"
file_location = str(os.getcwd()), "\\", "irr_analysis_results.txt"
file_location = "".join(file_location)

# csv file is written to include the following values below
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter = ' ', quotechar = "$", quoting = csv.QUOTE_MINIMAL) # Necessary to remove the quotation marks 
    csvwriter.writerow(("Filename given when saved in H2ORUN=", file_location))
    csvwriter.writerow(("Date of measurement=", date_measure_irr))
    csvwriter.writerow(('Time of measurement=', time_measure_irr))
    csvwriter.writerow(("Predrift time (s)=", time_pre))
    csvwriter.writerow(("Dissipation time (s)", time_dis))
    csvwriter.writerow(("Afterdrift time (s)", time_post))
    csvwriter.writerow(("Current decade box resistance=", R_burster))
    csvwriter.writerow(("1 Ohm calibration (V/ohm)=", ohm_calibration(time_pre_ohm, time_ohm, time_post_ohm, total_time_ohm, tme_ohm, voltages_ohm, pre_drift_ignore, post_drift_ignore, ohm_run_ignore)))
    csvwriter.writerow(("Change in voltage for irradiation run (V)=", deltaV(time_pre, time_dis, time_post, total_time, tme, voltages, R_burster, pre_drift_ignore, post_drift_ignore, T_cal)))
    csvwriter.writerow(("Change in temperature for irradiation run (K)=", deltaV_to_deltaT(deltaV(time_pre, time_dis, time_post, total_time, tme, voltages, R_burster, pre_drift_ignore, post_drift_ignore, T_cal), T_cal, R_burster)))
    csvwriter.writerow(("-------------------------------------------"))
    csvwriter.writerow(('Time (s)', 'Voltage (mV)'))
    for i in range(total_time + 1): 
        csvwriter.writerow((format(tme[i], '.7f'), format(voltages[i], '.7f')))
        
def replace_char(csv_line, old_char, new_char):
    return csv_line.replace(old_char, new_char)

with open('irr_analysis_results.csv') as f: # Also written to a .txt file for easier analysis in the future
    g = open("irr_analysis_results.txt", "w")
    for i, line in enumerate(f):
        a = replace_char(line, "$", "") # Each line is searched for the quote character "$" and removed using the function initialized above
        if not a.strip() == "":
            g.write(a)
    g.close()