# import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
from functions import *
from read_from_file import *

plt.xlabel('time (s)')
plt.ylabel('Temperature (celsius)')
plt.rcParams["figure.figsize"] = [20, 15]

if read_ohm_run_file:
    generator = read_ohm_file()
    time_pre_ohm = int(next(generator))
    time_ohm = int(next(generator))
    time_post_ohm = int(next(generator))
    total_time_ohm = time_pre_ohm + time_ohm + time_post_ohm
    next(generator)
    next(generator)
    tme_ohm = next(generator)
    voltages_ohm = next(generator)
    plt.plot(tme_ohm, voltages_ohm, c = 'red')
    plt.show()


plt.plot(tme_ohm[1:time_pre_ohm - 4],voltages_ohm[1:time_pre_ohm - 4], c='blue')
plt.plot(tme_ohm[time_pre_ohm + 5:total_time_ohm - time_post_ohm - 4],voltages_ohm[time_pre_ohm + 5:total_time_ohm - time_post_ohm - 4], c='black')
plt.plot(tme_ohm[time_pre_ohm + time_ohm + 5:total_time_ohm + 1],voltages_ohm[time_pre_ohm + time_ohm + 5:total_time_ohm +1], c='red')

