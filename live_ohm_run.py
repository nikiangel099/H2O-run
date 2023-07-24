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

counter = 0
prev = time.time()
while counter < total_time_ohm:
    curr = time.time()
    if counter == 0:
        tme_ohm.append(0)
        voltages_ohm.append(float(inst.query('Q')[:-2]))
    elif curr - prev < counter + 0.01 and curr - prev > counter:
        time_ohm.append(curr)
        voltages_ohm.append(float(inst.query('Q')[:-2]))
    prev = curr
    counter += 1
    plt.plot(tme_ohm, voltages_ohm)
    plt.show()