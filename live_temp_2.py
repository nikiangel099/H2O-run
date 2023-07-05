import cmath
import math
import pyvisa

rm = pyvisa.ResourceManager()
device = 'GPIB0::2::INSTR'  
inst = rm.open_resource(device)

beta1 = 3112.621146
beta2= 3120.790829

def sens1(t):
    global beta1
    beta = beta1
    if t < 273.15:
        t += 273.15
    return -beta / (t * t)

def sens2(t):
    global beta2
    beta = beta2
    if t < 273.15:
        t += 273.15
    return -beta / (t * t)


def RMS(a):
    ret = math.sqrt(a.real**2 + a.imag**2)
    return ret

def CMult(a, b):
    ret = complex(a.real * b.real - a.imag * b.imag, a.imag * b.real + b.imag * a.real)
    return ret

def CDiv(a, b):
    tmp = b.real**2 + b.imag**2
    ret = complex((a.real * b.real + a.imag * b.imag) / tmp, (a.imag * b.real - a.real * b.imag) / tmp)
    return ret

def CSum(a, b):
    ret = complex(a.real + b.real, a.imag + b.imag)
    return ret

def CDiff(a, b):
    ret = complex(a.real - b.real, a.imag - b.imag)
    return ret
def enter_Z(Ztype, value, freq):
    ret = complex(0.0, 0.0)
    if Ztype[0] == 'R':
        ret = complex(value, 0.0)
    elif Ztype[0] == 'C':
        ret = complex(0.0, -1.0 / (2 * math.pi * freq * value))
    elif Ztype[0] == 'L':
        ret = complex(0.0, 2 * math.pi * freq * value)
    else:
        print("Error: Ztype not recognized (R, C, or L ??)")
    return ret

def rterm(t_, it):
    r0_1 = 4386.01167
    r0_2 = 4496.510108
    global beta1
    global beta2
    ZERO_K = 273.15
    t0 = 25.0 + ZERO_K
    if it == 1:
        fw = r0_1 * math.exp(beta1 * (1.0 / t_ - 1.0 / t0))
    else:
        fw = r0_2 * math.exp(beta2 * (1.0 / t_ - 1.0 / t0))
    return fw

def signal(f, optemp, R_B, V_s, C_cp):
    EP = 0.00001
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
    R_add = 10000
    mK_per_uW1 = 2
    mK_per_uW2 = 2
    R_s = 51.5
    no_power = False
    THRESHOLD_LOW_HIGH = 6
    if optemp < 273.15:
        optemp += 273.15
    dRterm = 0
    dRterm_old = dRterm + 1
    if optemp < (THRESHOLD_LOW_HIGH + 273.15):
        ZR_add = enter_Z("R", float(R_add), f)

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
        Z_th1 = CDiv(CMult(ZR_th1, ZC_th1), CSum(ZR_th1, ZC_th1))
        
        R_th2 = rterm(optemp, 2) + dRterm2
        ZR_th2 = enter_Z("R", float(R_th2), f)
        Z_th2 = CDiv(CMult(ZR_th2, ZC_th2), CSum(ZR_th2, ZC_th2))
        
        Z_therm = CSum(Z_th1, Z_th2)
        Z_therm_keep1 = Z_therm
        Z_therm = CSum(Z_therm, ZR_tc)
        Z_therm_keep2 = Z_therm
        Z_therm = CDiv(CMult(Z_therm,ZC_tc),CSum(Z_therm,ZC_tc))
        Z_therm = CDiv(CMult(Z_therm,Z_LA),CSum(Z_therm,Z_LA))
        
        if optemp < (THRESHOLD_LOW_HIGH + 273.15):
            Z_A_add = CSum(Z_therm,ZR_add)
            Z_A_add = CDiv(CMult(Z_A_add,ZC_BA),CSum(Z_A_add,ZC_BA))
        else:
            Z_A_add = CDiv(CMult(Z_therm,ZC_BA),CSum(Z_therm,ZC_BA))
        
        Z_A = CSum(Z_A_add,ZR_B)
        Z_A = CDiv(CMult(Z_A,ZC_BB),CSum(Z_A,ZC_BB))
        Z_A = CDiv(CMult(Z_A,ZC_s),CSum(Z_A,ZC_s))
        
        Z_2 = CDiv(CMult(ZC_cp,ZR_2),CSum(ZC_cp,ZR_2))
        Z_2 = CDiv(CMult(Z_2,Z_LB),CSum(Z_2,Z_LB))
        Z_B = CSum(ZR_1,Z_2)
        
        Z_AB = CDiv(CMult(Z_A,Z_B),CSum(Z_A,Z_B))
        Ztotal = CSum(Z_AB,ZR_s)
        
        V_AB= CMult(V_s,CDiv(Z_AB, Ztotal));
        V_B = CMult(V_AB,CDiv(Z_2,Z_B));
        V_A_add = CMult(V_AB,CDiv(Z_A_add,CSum(Z_A_add,ZR_B)))
        V_A = CMult(V_A_add,CDiv(Z_therm,CSum(Z_therm,ZR_add)))
        
        if not no_power:

            I_therm = CDiv(V_A, Z_therm_keep2)
            V_therm = CMult(V_A, CDiv(Z_therm_keep1, Z_therm_keep2))

            P_therm1 = RMS(I_therm) * RMS(V_therm) * rterm(optemp, 1) / (rterm(optemp, 1) + rterm(optemp, 2))
            P_therm2 = RMS(I_therm) * RMS(V_therm) * rterm(optemp, 2) / (rterm(optemp, 1) + rterm(optemp, 2))

            dRterm1 = mK_per_uW1 * P_therm1 * 1.0e3 * rterm(optemp, 1) * sens1(optemp)
            dRterm2 = mK_per_uW2 * P_therm2 * 1.0e3 * rterm(optemp, 2) * sens2(optemp)
            dRterm += (dRterm1 + dRterm2 - dRterm_old)
       
        ret = complex(V_A.real - V_B.real, V_A.imag - V_B.imag)
        prV_A = V_A
        prV_B = V_B
        R_term = R_th1 + R_th2
        po1 = P_therm1
        po2 = P_therm2
        return ret
        
    
def calculate_T_vess(voff, m_bursterSetting, vpower, freq):
    dtemp = 0.1
    net_signal = complex(1.0e10, 0)
    vpower = 1
    Vexc = complex(vpower, 0)
    R_est = m_bursterSetting + voff / 25e-6
    T_vess = 1.0 / (1 / 298.15 + (math.log(R_est) - math.log(4500)) / 3126.142) - 273.15
    C_i = 1800.0
    i = 0
    
    while abs(net_signal.real - voff) > 1.0e-9 and i < 150:
        net_signal_old = net_signal.real - voff
        net_signal = signal(freq, T_vess, m_bursterSetting, Vexc, C_i)
        if abs(net_signal.real - voff) > 1.0e-9:
            if net_signal_old * (net_signal.real - voff) < 0.0:
                dtemp /= -2.0
            T_vess += dtemp
            i += 1
    
    if i > 90:
        chstr = f"Iterations: {i}\nT_Vessel: {T_vess}\nT_step: {dtemp}\nVoltage: {voff}"
        return "CONVERGENCE PROBLEM:" + chstr
    else:
        chstr = f"Iterations: {i}\nT_Vessel {T_vess}\nT_step: {dtemp}\nVoltage: {voff}"
        return "T_vessel() returns:" + chstr


voff= float((inst.query('Q'))[:-2])
m_bursterSetting = 19679
vpower = 1
freq = float((inst.query('F'))[:-2])
print(calculate_T_vess(voff, m_bursterSetting, vpower, freq))
                
    