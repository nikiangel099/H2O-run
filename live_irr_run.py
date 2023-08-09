import time
import pyvisa
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime, timezone
import pytz
from T_cal_calc import *

d = datetime.now(pytz.timezone("America/New_York"))
rm = pyvisa.ResourceManager()
device = 'GPIB0::2::INSTR'  # Device address of lock-in amplifier
inst = rm.open_resource(device)


# Below is pre, dis and post time intervals (s)
time_pre= 10
time_dis = 10
time_post = 10
total_time= time_pre + time_dis + time_post

# Need to find a way to initialize the burster setting in the interface, but just initialized the value below
bursterSetting = 19669

tme = []
voltages = []

curr_time = d.strftime("%X") # Initializes variable to the current time
T_cal_1 = measure_T_cal() # pre-irr T_cal is measured
# # Keep commented unless connected to GPIB device:
counter = 1
start = time.time()
tme.append(0)
voltages.append(float(inst.query('Q')[:-2])*1e3)
while counter < total_time + 1:
    curr = time.time()
    if (curr - start) > counter:
        tme.append(curr - start)
        voltages.append(float(inst.query('Q')[:-2])*1e3)
        counter += 1
        plt.plot(tme, voltages)
        plt.show()
        
T_cal_2 = measure_T_cal() # post-irr T_cal is measured
T_cal = (T_cal_1+T_cal_2)/2 # Average T_cal is taken

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
    csvwriter.writerow(('Time (s)', 'Voltage (microV)'))
    for i in range(total_time + 1): 
        csvwriter.writerow((format(tme[i], '.7f'), format(voltages[i], '.7f')))
    csvwriter.writerow(("Filename given when saved in H2ORUN=", file_location))
    csvwriter.writerow(("Date of measurement=", date))
    csvwriter.writerow(('Time of measurement=', curr_time))
    csvwriter.writerow(('Predrift time (s)=', time_pre))
    csvwriter.writerow(('Dissipation time (s)=', time_dis))
    csvwriter.writerow(('Afterdrift time (s)=', time_post))
    csvwriter.writerow(('Twater(K)=', T_cal))
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