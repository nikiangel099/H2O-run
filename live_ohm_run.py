import time
import pyvisa
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()
device = 'GPIB0::2::INSTR'  # Device address of lock-in amplifier
inst = rm.open_resource(device)

time_pre_ohm = 50
time_ohm = 50
time_post_ohm = 50
total_time_ohm = time_pre_ohm + time_ohm + time_post_ohm

tme_ohm = []
voltages_ohm = []

counter = 1
start = time.time()
tme_ohm.append(0)
voltages_ohm.append(float(inst.query('Q')[:-2]))
while counter < total_time_ohm + 1:
    curr = time.time()
    if (curr - start) > counter:
        tme_ohm.append(curr - start)
        voltages_ohm.append(float(inst.query('Q')[:-2]))
        counter += 1
        print(tme_ohm[counter-1], "    ", voltages_ohm[counter-1])
        plt.plot(tme_ohm, voltages_ohm)
        plt.show()
    