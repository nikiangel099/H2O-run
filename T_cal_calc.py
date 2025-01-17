import pyvisa
import math

# This file takes the four-series resistance and outputs the temperature of the calorimeter
# This T_cal calculation is needed for a live run of irradiation
def measure_T_cal():
    rm = pyvisa.ResourceManager()
    device = 'GPIB0::16::INSTR'  # Device address of multi-meter amplifier
    inst = rm.open_resource(device)
    
    inst.write("ROUTe:CLOSe (@3)") # # The below is not needed as T_cal is read from the irradiation run text file
    inst.write("ROUTe:OPEN (@3)")
    R_temp = float(inst.query(':MEASure:FRESistance?'))
    temp_probe = 3 # # The below constants are based on which RTD probe is used
    
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
        
    return (-1*AI+(math.sqrt((AI*AI)-(4*BI*(1-(R_temp/RI))))))/(2*BI)