
read_ohm_run_file = True
read_irr_run_file = True


def read_ohm_file():
    time_ohm = []
    voltage_ohm = []
    with open('ohm_run_example.txt') as f:
        for i, line in enumerate(f):
            if i>0 and line[1].isdigit():
                column = line.lstrip()
                column = column.split(' ')
                time_ohm.append(float(column[0].strip()))
                voltage_ohm.append(float(column[-1].strip()))
            if line.startswith('PreOHM time (s)'):
                parts = line.split('=')
                yield float(parts[1].strip())
            elif line.startswith('OHM time (s)'):
                parts = line.split('=')
                yield float(parts[1].strip())
            elif line.startswith('AfterOHM time (s)'):
                parts = line.split('=')
                yield float(parts[1].strip())
            elif line.startswith('Twater(K)'):
                parts = line.split('=')
                yield float(parts[1].strip())
            elif line.startswith('Current decade box resistance'):
                parts = line.split('=')
                yield float(parts[1].strip()) 
            
    yield time_ohm
    yield voltage_ohm
        
def read_irr_file():
    time_irr = []
    voltage_irr = []
    with open('irr_run_example.txt') as f:
        for i, line in enumerate(f):
            if i>0 and line[1].isdigit():
                column = line.lstrip()
                column = column.split(' ')
                time_irr.append(float(column[0].strip()))
                voltage_irr.append(float(column[-1].strip()))
            if line.startswith('Predrift time (s)'):
                parts = line.split('=')
                yield float(parts[1].strip())
            elif line.startswith('Dissipation time (s)'):
                parts = line.split('=')
                yield float(parts[1].strip())
            elif line.startswith('Afterdrift time (s)'):
                parts = line.split('=')
                yield float(parts[1].strip())
            elif line.startswith('Twater(K)'):
                parts = line.split('=')
                yield float(parts[1].strip())
            elif line.startswith('Decade box setting(OHM)'):
                parts = line.split('=')
                yield float(parts[1].strip())
            
    yield time_irr
    yield voltage_irr
            