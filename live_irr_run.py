import time
import pyvisa
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (12,6) # Figure size is set in inches (x, y) 
import csv
import os
from datetime import datetime
import pytz
#from T_cal_calc import *

d = datetime.now(pytz.timezone("America/New_York")) # Timezone is established for accurate date and time on documents
rm = pyvisa.ResourceManager()
device = 'GPIB0::2::INSTR'  # Device address of lock-in amplifier
inst = rm.open_resource(device)


# Below is pre, dis and post time intervals (s)
time_pre= 10
time_dis = 10
time_post = 10
total_time= time_pre + time_dis + time_post

# Need to find a way to initialize the burster setting in the interface
bursterSetting = 19669

# For the empty lists below, the live data will be stored for each second
tme = []
voltages = []

curr_time = d.strftime("%X") # Initializes variable to the current time
#T_cal_1 = measure_T_cal() # pre-irr T_cal is measured
# Only uncomment below when connected to GPIB device:
plt.ion() # Interactive plot
plt.xlabel('time (s)')
plt.ylabel('Voltage (mV)')
counter = 1
start = time.time() # Storing the starting time
tme.append(0) # First time(s) is 0 sec
voltages.append(float(inst.query('Q')[:-2])*1e3) # Voltage taken at 0 sec
plt.plot(tme, voltages)
plt.xlim(0, total_time) # Keeps the x axis from 0 to 30
plt.grid(True) # Gridlines are visible
plt.draw() # plt.draw() is used with plt.clf() to update the existing plot window
plt.pause(0.7) # Allow some time (0.7 sec) for next data to be collected 
while counter < total_time + 1: # While loop to keep data collection going while not exceeding total time
    curr = time.time() # Each time is collected to determine the elapsed time since starting
    if (curr - start) > counter: # If the next second is reached, the data is collected and plotted in this if statement
        plt.clf()
        tme.append(curr - start)
        voltages.append(float(inst.query('Q')[:-2])*1e3) # The voltage is queried and multiplied by 1e3 to store as mV
        counter += 1 # Next second is added
        plt.xlabel('time (s)')
        plt.ylabel('Voltage (mV)')
        plt.plot(tme, voltages)
        plt.xlim(0, total_time)
        plt.grid(True)
        plt.draw()
        plt.pause(0.7)
        
plt.ioff() # Interactive mode is turned off
plt.show() # Plot window remains open. Close plot window to exit the script
        
        
#T_cal_2 = measure_T_cal() # post-irr T_cal is measured
#T_cal = (T_cal_1+T_cal_2)/2 # Average T_cal is taken

# Below gets file location and current date of the file that will be displayed in the output analysis file
filename = "live_irr_run_to_file.csv"
file_location = str(os.getcwd()), "\\", "live_irr_run_to_file.txt"
file_location = "".join(file_location)
date = d.strftime("%A"), " ", d.strftime("%b"), " ", d.strftime("%d"), " ", d.strftime("%Y")
date = "".join(date)
date = "".join(date)

# csv file is written to include the following values below
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter = ',', escapechar = "$", quoting = csv.QUOTE_NONE) # Necessary to remove the quotation marks 
    csvwriter.writerow(('Time (s)', 'Voltage (mV)'))
    for i in range(total_time + 1): 
        csvwriter.writerow((format(tme[i], '.7f'), format(voltages[i], '.7f')))
    csvwriter.writerow(("Filename given when saved in H2ORUN=", file_location))
    csvwriter.writerow(("Date of measurement=", date))
    csvwriter.writerow(('Time of measurement=', curr_time))
    csvwriter.writerow(('Predrift time (s)=', time_pre))
    csvwriter.writerow(('Dissipation time (s)=', time_dis))
    csvwriter.writerow(('Afterdrift time (s)=', time_post))
    #csvwriter.writerow(('Twater(K)=', T_cal))
    csvwriter.writerow(('Decade box setting(OHM)=', bursterSetting))

    
def replace_char(csv_line, old_char, new_char):
    return csv_line.replace(old_char, new_char)

with open('live_irr_run_to_file.csv') as f: # Also written to a .txt file for easier analysis in the future
    g = open("live_irr_run_to_file.txt", "w")
    for i, line in enumerate(f): 
        a = replace_char(line, ",", " ") # Each line is searched for the quote character "$" and removed using the function initialized above
        if not a.strip() == "":
            g.write(a)
    g.close()