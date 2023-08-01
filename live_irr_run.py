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

counter = 1
start = time.time()
tme.append(0)
voltages.append(float(inst.query('Q')[:-2]))
while counter < total_time+ 1:
    curr = time.time()
    if (curr - start) > counter:
        tme.append(curr - start)
        voltages.append(float(inst.query('Q')[:-2]))
        counter += 1
        print(tme[counter-1], "    ", voltages[counter-1])
        plt.plot(tme, voltages)
        plt.show()
    