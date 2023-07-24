import time
import pyvisa
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()
device = 'GPIB0::2::INSTR'  # Device address of lock-in amplifier
inst = rm.open_resource(device)

time_pre = 60
time_dis = 20
time_post = 60
total_time = time_pre + time_dis + time_post

tme = []
voltages = []

counter = 0
prev = time.time()
while counter < total_time:
    curr = time.time()
    if counter == 0:
        tme.append(0)
        voltages.append(float(inst.query('Q')[:-2]))
    elif curr - prev < counter + 0.01 and curr - prev > counter: # Queries device every second
        time.append(curr)
        voltages.append(float(inst.query('Q')[:-2]))
    prev = curr
    counter += 1
    plt.plot(tme, voltages)
    plt.show()