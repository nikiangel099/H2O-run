from read_from_file import *
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

# Seconds of pre, dis, and post to ignore in linear fit
pre_drift_ignore = 5
post_drift_ignore = 5
ohm_run_ignore = 2

# # Ohm run variables are read from read_from_file.py
generator = read_ohm_file(filename_ohm) # read_ohm_file() becomes a generator object
date_measure_ohm = next(generator) # First yield result is given to variable date of measurement
time_measure_ohm = next(generator)
time_pre_ohm = int(next(generator)) 
time_ohm = int(next(generator))
time_post_ohm = int(next(generator))
total_time_ohm = time_pre_ohm + time_ohm + time_post_ohm
tme_ohm = next(generator)
voltages_ohm = next(generator)

# # Uncomment below to check if the variables from the text file is correct
# print(date_measure_ohm, time_measure_ohm, time_pre_ohm, time_ohm, time_post_ohm, total_time_ohm, tme_ohm, voltages_ohm)
    
# Plots are created below for visual confirmation
plt.xlabel('time (s)')
plt.ylabel('Voltage (mV)')
plt.rcParams["figure.figsize"] = [20, 15]
plt.plot(tme_ohm, voltages_ohm) # All time and voltage data points are plotted
plt.show()
    

plt.xlabel('time (s)')
plt.ylabel('Voltage (mV)')
plt.rcParams["figure.figsize"] = [20, 15]
plt.plot(tme_ohm[1:time_pre_ohm - pre_drift_ignore + 1],voltages_ohm[1:time_pre_ohm - pre_drift_ignore + 1], c='blue') # Pre-drift is plotted in blue 
plt.plot(tme_ohm[time_pre_ohm + ohm_run_ignore:total_time_ohm - time_post_ohm - ohm_run_ignore + 1],voltages_ohm[time_pre_ohm + ohm_run_ignore:total_time_ohm - time_post_ohm - ohm_run_ignore + 1], c='black') # Duration of 1 ohm gain is plotted in black
plt.plot(tme_ohm[time_pre_ohm + time_ohm + post_drift_ignore:total_time_ohm + 1],voltages_ohm[time_pre_ohm + time_ohm + post_drift_ignore:total_time_ohm +1], c='red') # Post-drift is plotted in red
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

deltaV_deltaR = ohm_calibration(time_pre_ohm, time_ohm, time_post_ohm, total_time_ohm, tme_ohm, voltages_ohm, pre_drift_ignore, post_drift_ignore, ohm_run_ignore)

# File location where ohm run analysis result is saved is extracted below
filename = "ohm_analysis_results.csv"
file_location = str(os.getcwd()), "\\", "ohm_analysis_results.txt"
file_location = "".join(file_location)

# csv file is written to include the following values below
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter = ',', escapechar = "$", quoting = csv.QUOTE_NONE) # Necessary to remove the quotation marks 
    csvwriter.writerow(("Filename given when saved in H2ORUN=", file_location))
    csvwriter.writerow(("Date of measurement=", date_measure_ohm))
    csvwriter.writerow(('Time of measurement=', time_measure_ohm))
    csvwriter.writerow(("PreOHM time (s)=", time_pre_ohm))
    csvwriter.writerow(("OHM time (s)=", time_ohm))
    csvwriter.writerow(("AfterOHM time (s)=", time_post_ohm))
    csvwriter.writerow(("1 Ohm calibration (V/ohm)=", deltaV_deltaR))
    csvwriter.writerow(("-------------------------------------------"))
    csvwriter.writerow(('Time (s)', 'Voltage (mV)'))
    for i in range(total_time_ohm + 1): 
        csvwriter.writerow((format(tme_ohm[i], '.7f'), format(voltages_ohm[i], '.7f')))
        
def replace_char(csv_line, old_char, new_char):
    return csv_line.replace(old_char, new_char)

with open('ohm_analysis_results.csv') as f: # Also written to a .txt file for easier analysis in the future
    g = open("ohm_analysis_results.txt", "w")
    for i, line in enumerate(f):
        a = replace_char(line, ",", " ") # Each line is searched for the quote character "$" and removed using the function initialized above
        if not a.strip() == "":
            g.write(a)
    g.close()
