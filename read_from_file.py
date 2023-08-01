# Functions to read the values from a text file

def replace_char(csv_line, old_char, new_char):
    return csv_line.replace(old_char, new_char)

def read_ohm_file():
    time_ohm = []
    voltage_ohm = []
    with open('live_ohm_run_to_file.txt') as f:
        for i, line in enumerate(f): # Each line is searched for the variables or data points
            if i>0 and line[4].isdigit(): # The time and voltage data starts at the second row, it is determined to be a data point as long as the second element is a digit (some first elements of each row is whitespace)
                column = line.lstrip() # The leading whitespaces are removed (see previous comment)
                column = column.split(' ') # The time and voltage are separated by a space in the line, becomes seperate elements using .split()
                time_ohm.append(float(column[0].strip())) # Time is added to list
                voltage_ohm.append(float(column[-1].strip())) # Voltage is added to list
            if line.startswith('PreOHM time (s)'): # Variable name is searched in line
                parts = line.split('=') # Equal sign is the separation from the variable name and variable value
                yield float(parts[1].strip()) # The variable value is being output from the function as a yield
            elif line.startswith('OHM time (s)'):
                parts = line.split('=')
                yield float(parts[1].strip())
            elif line.startswith('AfterOHM time (s)'):
                parts = line.split('=')
                yield float(parts[1].strip())
            
    yield time_ohm
    yield voltage_ohm


def read_irr_file():
    time_irr = []
    voltage_irr = []
    with open('live_irr_run_to_file.txt') as f:
        for i, line in enumerate(f):
            if i>0 and line[4].isdigit():
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
            
