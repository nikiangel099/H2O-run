import time
import pyvisa
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (12,6) # Figure size is set in inches (x, y) 
import csv
import os
from datetime import datetime, timezone
import pytz

d = datetime.now(pytz.timezone("America/New_York")) # Timezone is established for accurate date and time on documents

# Keep commented unless connected to GPIB device:
rm = pyvisa.ResourceManager()
device = 'GPIB0::2::INSTR'  # Device address of lock-in amplifier
inst = rm.open_resource(device)

# Below is pre, dis and post time intervals (s)
time_pre_ohm = 10
time_ohm = 10
time_post_ohm = 10
total_time_ohm = time_pre_ohm + time_ohm + time_post_ohm
# Need to find a way to initialize the burster setting in the interface
bursterSetting = 19669

# For the empty lists below, the live data will be stored for each second
tme_ohm = []
voltages_ohm = []
# voltages_ohm = [0.00012] * (total_time_ohm + 1) # Made up voltages to run code without being connected to gpib device

# for i in range(total_time_ohm + 1):
#     tme_ohm.append(i) # Made up time 

curr_time = d.strftime("%X") # Initializes variable to the current time

# Only uncomment below when connected to GPIB device:
plt.ion() # Interactive plot
plt.xlabel('time (s)')
plt.ylabel('Voltage (mV)')
counter = 1
start = time.time() # Storing the starting time
tme_ohm.append(0) # First time(s) is 0 sec
voltages_ohm.append(float(inst.query('Q')[:-2])*1e3) # Voltage taken at 0 sec
plt.plot(tme_ohm, voltages_ohm)
plt.xlim(0, total_time_ohm) # Keeps the x axis from 0 to 30
plt.grid(True) # Gridlines are visible
plt.draw() # plt.draw() is used with plt.clf() to update the existing plot window
plt.pause(0.7) # Allow some time (0.7 sec) for next data to be collected 
while counter < total_time_ohm + 1: # While loop to keep data collection going while not exceeding total time
    curr = time.time() # Each time is collected to determine the elapsed time since starting
    if (curr - start) > counter: # If the next second is reached, the data is collected and plotted in this if statement
        plt.clf()
        tme_ohm.append(curr - start)
        voltages_ohm.append(float(inst.query('Q')[:-2])*1e3) # The voltage is queried and multiplied by 1e3 to store as mV
        counter += 1 # Next second is added
        plt.xlabel('time (s)')
        plt.ylabel('Voltage (mV)')
        plt.plot(tme_ohm, voltages_ohm)
        plt.xlim(0, total_time_ohm)
        plt.grid(True)
        plt.draw()
        plt.pause(0.7)
        
plt.ioff() # Interactive mode is turned off
plt.show() # Plot window remains open. Close plot window to exit the script
        

# Below gets file location and current date of the file that will be displayed in the output analysis file
filename = "live_ohm_run_to_file.csv"
file_location = str(os.getcwd()), "\\", "live_ohm_run_to_file.txt"
file_location = "".join(file_location)
date = d.strftime("%A"), " ", d.strftime("%b"), " ", d.strftime("%d"), " ", d.strftime("%Y")
date = "".join(date)
date = "".join(date)

# csv file is written to include the following values below
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter = ',', escapechar = "$", quoting = csv.QUOTE_NONE) # Necessary to remove the quotation marks 
    csvwriter.writerow(('Time (s)', 'Voltage (mV)'))
    for i in range(total_time_ohm + 1): 
        csvwriter.writerow((format(tme_ohm[i], '.7f'), format(voltages_ohm[i], '.7f')))
    csvwriter.writerow(("Filename given when saved in H2ORUN=", file_location))
    csvwriter.writerow(("Date of measurement=", date))
    csvwriter.writerow(('Time of measurement=', curr_time))
    csvwriter.writerow(("PreOHM time (s)=", time_pre_ohm))
    csvwriter.writerow(("OHM time (s)=", time_ohm))
    csvwriter.writerow(("AfterOHM time (s)=", time_post_ohm))
    csvwriter.writerow(("Current decade box resistance=", bursterSetting))

    
def replace_char(csv_line, old_char, new_char): # Created function for fast character replacement which is used in the following lines
    return csv_line.replace(old_char, new_char)

with open('live_ohm_run_to_file.csv') as f: # Also written to a .txt file for easier analysis in the future
    g = open("live_ohm_run_to_file.txt", "w")
    for i, line in enumerate(f):  # Each line is searched for the quote character "$" and removed using the function initialized above
        a = replace_char(line, ",", " ")
        if not a.strip() == "":
            g.write(a)
    g.close()
    