import pyvisa

rm = pyvisa.ResourceManager()
device = 'GPIB0::2::INSTR'  # Replace with your device address
inst = rm.open_resource(device)

inst.write('P 0')
inst.write('S 0')
inst.write('A 0')
inst.write('O 0')
inst.write('B 0')
inst.write('C 1')
inst.write('D 1')
inst.write('G 12')
inst.write('M 0')
inst.write('R 1')
inst.write('I 0')
inst.write('T 6 ,2')
inst.write('L 1 ,0')
inst.write('L 2 ,0')
inst.write('X 1')
inst.write('E 0')