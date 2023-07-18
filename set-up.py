import pyvisa # Module allows remote communication with GPIB device

rm = pyvisa.ResourceManager()
device = 'GPIB0::2::INSTR'  # Device address of lock-in amplifier
inst = rm.open_resource(device)

inst.write('P 0') # Sets the phase setting to 0 degrees
inst.write('S 0') # Sets parameter shown on the analog meter and output digital display of 'X' as well as the output BNC
inst.write('A 0') # Sets the auto-offset function to 'off'
inst.write('O 0') # Sets the offset to 'off'
inst.write('B 0') # Sets the bandpass filter to be taken out
inst.write('C 1') # Sets the reference LCD display to show the phase setting
inst.write('D 1') # Sets the dynamic reserve to 'NORM'
inst.write('G 12') # Sets the gain (sensitivity) to 50 microvolts
inst.write('M 0') # Sets the reference mode to 'f'
inst.write('R 1') # Sets the reference input trigger mode to 'Symmetric'
inst.write('I 1') # Sets the local remote status to 'remote': front panel keys are not operative. 
                  # The display up key returns the status to local
inst.write('T 6 ,2') # Sets the status of the time constants
                     # pre-time constant: 300 ms, post-time constant: 1 s
inst.write('L 1 ,0') # Sets the status of the line notch filters
inst.write('L 2 ,0')
inst.write('X 1')
inst.write('E 0')
