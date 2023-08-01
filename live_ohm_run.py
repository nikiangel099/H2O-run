import time
import pyvisa
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime, timezone
import pytz

d = datetime.now(pytz.timezone("America/New_York"))
# rm = pyvisa.ResourceManager()
# device = 'GPIB0::2::INSTR'  # Device address of lock-in amplifier
# inst = rm.open_resource(device)

time_pre_ohm = 50
time_ohm = 50
time_post_ohm = 50
total_time_ohm = time_pre_ohm + time_ohm + time_post_ohm
bursterSetting = 19669

tme_ohm = []
voltages_ohm = [0.00012]*150

for i in range(150):
    tme_ohm.append(i)

curr_time = d.strftime("%X")

# counter = 1
# start = time.time()
# tme_ohm.append(0)
# voltages_ohm.append(float(inst.query('Q')[:-2]))
# while counter < total_time_ohm + 1:
#     curr = time.time()
#     if (curr - start) > counter:
#         tme_ohm.append(curr - start)
#         voltages_ohm.append(float(inst.query('Q')[:-2]))
#         counter += 1
#         plt.plot(tme_ohm, voltages_ohm)
#         plt.show()

filename = "live_ohm_run_to_file.csv"
file_location = str(os.getcwd()), "\\", "live_ohm_run_to_file.txt"
file_location = "".join(file_location)
date = d.strftime("%A"), ", ", d.strftime("%b"), " ", d.strftime("%d"), ", ", d.strftime("%Y")
date = "".join(date)
date = "".join(date)

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter = ' ', quotechar = "$", quoting = csv.QUOTE_MINIMAL)
    csvwriter.writerow(('Time (s)', 'Voltage (microV)'))
    for i in range(total_time_ohm): 
        csvwriter.writerow((format(tme_ohm[i], '.7f'), format(voltages_ohm[i], '.7f')))
    csvwriter.writerow(("Filename given when saved in H2ORUN=", file_location))
    csvwriter.writerow(("Date of measurement=", date))
    csvwriter.writerow(('Time of measurement=', curr_time))
    csvwriter.writerow(("PreOHM time (s)=", time_pre_ohm))
    csvwriter.writerow(("OHM time (s)=", time_ohm))
    csvwriter.writerow(("AfterOHM time (s)=", time_post_ohm))
    csvwriter.writerow(("Current decade box resistance=", bursterSetting))

    
def replace_char(csv_line, old_char, new_char):
    return csv_line.replace(old_char, new_char)

with open('live_ohm_run_to_file.csv') as f:
    g = open("live_ohm_run_to_file.txt", "w")
    for i, line in enumerate(f): # Each line is searched for the variables or data points
        a = replace_char(line, "$", "")
        if not a.strip() == "":
            g.write(a)
    g.close()
    