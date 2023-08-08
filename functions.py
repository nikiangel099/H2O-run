import math
import pyvisa

# Translated from the C++ functions, I am still not exactly clear what each section is for
# Ignore this .py file for now

def access_lock_in_amplifier():
    rm = pyvisa.ResourceManager()
    device = 'GPIB0::2::INSTR'  # Device address for lock-in amplifier
    return rm.open_resource(device)

def access_multimeter():
    rm = pyvisa.ResourceManager()
    device = 'GPIB0::16::INSTR' # Device address for multimeter
    return rm.open_resource(device)

def sens1(t): # Used in signal() below
    if t < 273.15:
        t += 273.15
    return -3112.621146 / (t * t) # -beta1/(t^2)

def sens2(t):
    if t < 273.15:
        t += 273.15
    return -3120.790829 / (t * t) # -beta2/(t^2)

def enter_Z(Ztype, value, freq): # Used in signal() below
    ret = complex(0.0, 0.0)
    if Ztype[0] == 'R':
        ret = complex(value, 0.0)
    elif Ztype[0] == 'C':
        ret = complex(0.0, -1.0 / (2 * math.pi * freq * value))
    elif Ztype[0] == 'L':
        ret = complex(0.0, 2 * math.pi * freq * value)
    return ret

def rterm(t_, it): # Used in signal() below
    r0_1 = 4386.01167
    r0_2 = 4496.510108
    beta1 = 3112.621146
    beta2 = 3120.790829
    ZERO_K = 273.15
    t0 = 25 + ZERO_K
    if it == 1:
        fw = r0_1 * math.exp(beta1 * (1.0 / t_ - 1.0 / t0))
    else:
        fw = r0_2 * math.exp(beta2 * (1.0 / t_ - 1.0 / t0))
    return fw

def signal(f, optemp, R_B, V_s, C_cp):
    EP = 0.00001 # epsilon
    # below are the NRC defines for the lock-in amplifier and the cabling
    R_1 = 10000.21 
    R_2 = 999.77
    C_LA = 180 + 20
    C_LB = 180 + 20
    R_LA = 10.11E6
    R_LB = 10.15E6
    C_th1 = 100
    C_th2 = 260
    C_BB = 70
    C_BA = 70
    C_s = 180
    R_tc = 3.33
    C_tc = 1330
    mK_per_uW1 = 2
    mK_per_uW2 = 2
    R_s = 51.5
    no_power = False
    if optemp < 273.15: #To Kelvin
        optemp += 273.15
    dRterm = 0
    dRterm_old = dRterm + 1

    ZR_B = enter_Z("R", float(R_B), f)
    ZC_BA = enter_Z("C", float(C_BA * 1.0e-12), f)
    ZC_BB = enter_Z("C", float(C_BB * 1.0e-12), f)
    ZC_s = enter_Z("C", float(C_s * 1.0e-12), f)
    ZR_1 = enter_Z("R", float(R_1), f)
    ZR_2 = enter_Z("R", float(R_2), f)
    ZC_LA = enter_Z("C", float(C_LA * 1.0e-12), f)
    ZR_LA = enter_Z("R", float(R_LA), f)
    Z_LA = ZC_LA * ZR_LA / (ZC_LA + ZR_LA)
    ZC_LB = enter_Z("C", float(C_LB * 1.0e-12), f)
    ZR_LB = enter_Z("R", float(R_LB), f)
    Z_LB = ZC_LB * ZR_LB / (ZC_LB + ZR_LB)
    ZR_s = enter_Z("R", float(R_s), f)
    ZR_tc = enter_Z("R", float(R_tc), f)
    ZC_tc = enter_Z("C", float(C_tc * 1.0e-12), f)
    ZC_th1 = enter_Z("C", float(C_th1 * 1.0e-12), f)
    ZC_th2 = enter_Z("C", float(C_th2 * 1.0e-12), f)
    ZC_cp = enter_Z("C", float(C_cp * 1.0e-12), f)
    
    dRterm1 = 0
    dRterm2 = 0
    
    while abs(dRterm_old - dRterm) > EP:
        dRterm_old = dRterm1
        R_th1 = rterm(optemp, 1) + dRterm1
        ZR_th1 = enter_Z("R", float(R_th1), f)
        Z_th1 = (ZR_th1 * ZC_th1) / (ZR_th1 + ZC_th1)
        
        R_th2 = rterm(optemp, 2) + dRterm2
        ZR_th2 = enter_Z("R", float(R_th2), f)
        Z_th2 = (ZR_th2 * ZC_th2) / (ZR_th2 + ZC_th2)
        
        Z_therm = Z_th1 + Z_th2
        Z_therm_keep1 = Z_therm
        Z_therm = Z_therm + ZR_tc
        Z_therm_keep2 = Z_therm
        Z_therm = (Z_therm * ZC_tc) / (Z_therm + ZC_tc)
        Z_therm = (Z_therm * Z_LA) / (Z_therm + Z_LA)
        Z_A_add = (Z_therm * ZC_BA) / (Z_therm + ZC_BA)
        
        Z_A = Z_A_add + ZR_B
        Z_A = (Z_A * ZC_BB) / (Z_A + ZC_BB)
        Z_A = (Z_A * ZC_s) / (Z_A + ZC_s)
        
        Z_2 = (ZC_cp * ZR_2) / (ZC_cp + ZR_2)
        Z_2 = (Z_2 * Z_LB) / (Z_2 + Z_LB)
        Z_B = ZR_1 + Z_2
        
        Z_AB = (Z_A * Z_B) / (Z_A + Z_B)
        Ztotal = Z_AB + ZR_s

        V_AB= V_s * (Z_AB / Ztotal);
        V_B = V_AB * (Z_2 / Z_B);
        V_A_add = V_AB * Z_A_add / (Z_A_add + ZR_B)
        V_A = V_A_add
        
        if not no_power:

            I_therm = (V_A / Z_therm_keep2)
            V_therm = (V_A * (Z_therm_keep1 / Z_therm_keep2))

            P_therm1 = abs(I_therm) * abs(V_therm) * rterm(optemp, 1) / (rterm(optemp, 1) + rterm(optemp, 2))
            P_therm2 = abs(I_therm) * abs(V_therm) * rterm(optemp, 2) / (rterm(optemp, 1) + rterm(optemp, 2))

            dRterm1 = mK_per_uW1 * P_therm1 * 1.0e3 * rterm(optemp, 1) * sens1(optemp)
            dRterm2 = mK_per_uW2 * P_therm2 * 1.0e3 * rterm(optemp, 2) * sens2(optemp)
            dRterm += (dRterm1 + dRterm2 - dRterm_old)
       
        ret = complex(V_A.real - V_B.real, V_A.imag - V_B.imag)
        
        return ret
        
    
def calculate_T_vess(voff, m_bursterSetting, vpower, freq, C_i):
    dtemp = 0.1 # Initial temperature step of 0.1 deg C
    net_signal = complex(0, 0)
    i = 0 # counter
    R_est = m_bursterSetting + voff / 25e-6
    T_vess = 1.0 / (1 / 298.15 + (math.log(R_est) - math.log(9000)) / 3000) - 273.15 # Same formula given in the original files
    Vexc = complex(vpower, 0)
    
    while abs(net_signal.imag - voff) > 1.0e-9 and abs(dtemp) > 1e-8 and i < 100: # Loop continues until 100 iterations but can stop early due to the other conditions
        net_signal_old = net_signal.imag - voff
        net_signal = signal(freq, T_vess, m_bursterSetting, Vexc, C_i)
        if abs(net_signal.imag - voff) > 1.0e-9:
            if net_signal_old*(net_signal.imag - voff) < 0.0000001:
                dtemp /= -2 # abs(dtemp) decreases in this if statement
            T_vess += dtemp
            i += 1
            
    return T_vess


def adjusted_C_i():
    net_signal = complex(0,1.0e10)
    C_i = 1
    dC_i = 100.0
    m_bursterSetting = 19668
    # inst = access_lock_in_amplifier()
    # freq = float((inst.query('F'))[:-2])
    freq = 9.81
    voff=5e-6
    # for i in range(10):
    #     voff += float((inst.query('Q'))[:-2])
    # voff = voff/10
    
    vpower = 1
    Vexc = complex(vpower, 0)
    R_est = m_bursterSetting + voff / 25e-6
    T_vess = 1.0 / (1 / 298.15 + (math.log(R_est) - math.log(9000)) / 3000) - 273.15
    
    while abs(net_signal.imag) > 1.0e-8:
        net_signal_old = net_signal.imag
        net_signal = signal(freq, T_vess, m_bursterSetting, Vexc, C_i)
    
        if (net_signal_old * net_signal.imag) < 0.0:
            dC_i /= -2.0
        C_i -= dC_i

    return C_i
        
ad_C_i = adjusted_C_i()

voff = 5e-6 # Made up these values for now
m_bursterSetting = 19669
vpower = 1
freq = 9.81

# print(calculate_T_vess(voff, m_bursterSetting, vpower, freq, ad_C_i))
                
    
