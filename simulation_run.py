import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
import pyformulas as pf
import sys
import pandas as pd
import plotly.express as px
import math


time_pre = 20
time_dis = 20
time_post = 20
rounds = 1
total_time = time_pre + time_dis + time_post
rm = pyvisa.ResourceManager()
device = 'GPIB0::2::INSTR'  
inst = rm.open_resource(device)

voltages = []
tme=[]
plt.xlabel('time (s)')
plt.ylabel('Voltage (volts)')
plt.rcParams["figure.figsize"] = [20, 15]
counter = 0
prev = time.time()
while counter!= total_time*rounds + 1:
    x = time.time()
    if (x - prev) < (counter + 0.1) and counter < (x - prev ):
        y = float((inst.query('Q'))[:-2])
        tme.append(x - prev)
        voltages.append(y)
        plt.plot(tme, voltages, c = 'red')
        plt.show()
        print(tme[-1])
        counter += 1
plt.close()


delta_volt_list = []
for i in range(1, rounds + 1):

    a, b = np.polyfit(tme[total_time*(i-1)+1:time_pre + total_time *(i-1) - 4],voltages[total_time*(i-1)+1:time_pre + total_time*(i-1) - 4], 1)
    plt.plot(tme[total_time*(i-1)+1:time_pre + total_time*(i-1) - 4],voltages[total_time*(i-1)+1:time_pre + total_time*(i-1) - 4], c='blue')
    pre_volt = a * (total_time * i -time_dis-time_post + 0.5*time_dis)+b
    plt.scatter(total_time * i -time_dis-time_post + 0.5*time_dis, pre_volt)
       
    a, b = np.polyfit(tme[time_pre + time_dis + total_time*(i-1) + 5:total_time*i+1],voltages[time_pre + time_dis + total_time*(i-1) + 5:total_time*i+1], 1)
    plt.plot(tme[time_pre + time_dis + total_time*(i-1) + 5:total_time*i+1],voltages[time_pre + time_dis + total_time*(i-1) + 5:total_time*i+1], c='red')
    post_volt = a * (total_time * i -time_dis-time_post + 0.5*time_dis)+b
    plt.scatter(total_time * i -time_dis-time_post + 0.5*time_dis, post_volt)
    delta_volt_list.append(post_volt - pre_volt)

print(delta_volt_list)

device = 'GPIB0::16::INSTR'  
inst = rm.open_resource(device)
inst.write("ROUTe:CLOSe (@1)")
R_temp = float(inst.query(':MEASure:FRESistance?'))

temp_probe = input("Which temperature probe are you using? Enter an int 1-5 \n" )

if int(temp_probe) == 1:
    AI = 0.003942247616179
    BI = -2.06E-06
    RI = 99.87328
elif int(temp_probe) == 2:
    AI = 0.003931584
    BI = -1.8364E-06
    RI = 99.937458
elif int(temp_probe) == 3:
    AI = 0.00385991
    BI = -1.089E-06
    RI = 100.039338
elif int(temp_probe) == 4:
    AI = 3.86763e-3
    BI = 4.73227e-6
    RI = 100.04722
else:
    AI = 3.89020e-3
    BI = 2.09532e-6
    RI = 100.04198

T_cal = (-1*AI+(math.sqrt((AI*AI)-(4*BI*(1-(R_temp/RI))))))/(2*BI)

R_burster = float(input("What is the burster resistance displayed? "))
beta = 3112.621146
deltaV_deltaR = 25
delta_T= [0]*len(delta_volt_list)

for i in range(len(delta_volt_list)):
    delta_T[i] = (delta_volt_list[i]*T_cal**2)/(deltaV_deltaR*R_burster*beta)

print(f"The difference in temperatures are {delta_T}")

c_wp = 4.184
k_ht = 1
k_per = 1
k_dd = 1
k_rho = 1
k_hd = 2

D_w = [0]*len(delta_volt_list)
for i in range(len(delta_volt_list)):
    D_w[i] = c_wp*delta_T[i]*k_ht*k_per*k_dd*k_rho*k_hd

print(f"Dose to water is {D_w}")





#plt.axis([0, 120, -0.009, 0.009])
# voltage = [0]
# tme=[0]
# plt.rcParams["figure.figsize"] = [10, 15]
# plt.xlabel('time (s)')
# plt.ylabel('Voltage (volts)')
# fig = plt.figure()
# ax = fig.add_subplot(111)
# voltage_time = ax.plot(tme, voltage)
# for i in range(121):
#     voltage.append(float((inst.query('Q'))[:-2]))
#     x = time.time()
#     if i == 0:
#         prev = x
#         voltage[0] = (float((inst.query('Q'))[:-2]))
#     else:
#         voltage.append(float((inst.query('Q'))[:-2]))
#         tme.append(x - prev)
#     fig.canvas.draw()
#     fig.canvas.flush_events()
#     if i == 0:
#         plt.pause(0.95)
#     else:
#         plt.pause(0.992)
#     print(tme[i])
# plt.close()
# sys.exit()


# # Set up the plot
# ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')
# ax.set_xlim(0, 10)  # Set the x-axis limits
# ax.set_ylim(0, 10)  # Set the y-axis limits

# # Create the plot line
# line, = ax.plot(times, voltages, 'b-')

# for i in range(500):
#     if i == 1:
#         start_time=time.time()
#     voltages.append(inst.query(':MEASure:FRESistance?'))
#     times.append(start_time - time.time())
#     line.set_data(times, voltages)

#     # Adjust the plot view
#     ax.relim()
#     ax.autoscale_view()

#     time.sleep(1)
    
# plt.ioff()
# plt.show()



# instrument.baud_rate= 9600
# instrument.data_bits=8
# instrument.stop_bits = pyvisa.constants.StopBits.one
# instrument.parity = pyvisa.constants.Parity.none
# instrument.read_termination = chr(24)   #specified in the manual

# instrument.write(chr(33))    # command to get the serial number
# instrument.read()            # this works!

#instrument.write(chr(27))
# instrument.baud_rate = 9600
# instrument.read_termination = '<cr>'
# instrument.write_termination = '<cr>'
# instrument.query_delay = 30
# instrument.timeout = 60000
# instrument.write(":UNIT:TEMPerature?")
# import time
# instrument.write(":MEASure:FRESistance:CONTinuous ON")
# instrument.write(":MEASure:FRESistance:CONTinuous:TIME 10")

# # Start the continuous measurements
# instrument.write(":MEASure:FRESistance:CONTinuous:STARt")

# # Wait for the specified duration
# time.sleep(10)
# start_time = time.time()
# end_time = start_time + 30

#while time.time() < end_time:
# Stop the continuous measurements
#instrument.write(":MEASure:TEMPerature:CONTinuous:STOP")

# Read the final temperature value
    
    # instrument.write("ROUTe:OPEN (@1)")
    # instrument.write(":MEASure:FRESistance?")
    # print(instrument.read())
    # instrument.write("ROUTe:CLOSe (@1)")
    # # instrument.write("ROUTe:CLOSe (@1)")
    # # instrument.write("ROUTe:OPEN (@2)")
    # instrument.write(":MEASure:FRESistance?")
    # print(instrument.read())
    # instrument.write("ROUTe:CLOSe (@2)")
    # instrument.write("ROUTe:OPEN (@3)")
    # instrument.write(":MEASure:FRESistance?")
    # print(instrument.read())
    # instrument.write("ROUTe:CLOSe (@3)")
#response = instrument.read()
#instrument.write(':MEASure:VOLTage:AC')
#instrument.write(':TEMPerature?')
#time.sleep(1)
    


#print(instrument.read_bytes(16))
#print(pymeasure.inst.list_resources())
# for i in list(range(0,30)):
#     try:
#         inst = rm.open_resource('GPIB0::' +str(i) +'::INSTR')
#         print(inst.query("*IDN?"))
#     except:
    
#         print(i)
# 
#print(inst)
# print(inst.query(' *IDN?\n'))

# def read_all(devicehandle):

#     with devicehandle.ignore_warning(constants.VI_SUCCESS_DEV_NPRESENT, constants.VI_SUCCESS_MAX_CNT):

#         try:
#             data , status = devicehandle.visalib.read(devicehandle.session, devicehandle.bytes_in_buffer)
#         except:
#             pass
#     return data

# print(read_all(inst))