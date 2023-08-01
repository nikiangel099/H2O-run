time_ohm = []
voltage_ohm = []

def replace_char(csv_line, old_char, new_char):
    return csv_line.replace(old_char, new_char)

filename = "transfer_to_text.txt"
with open('live_ohm_run_to_file.csv') as f:
    g = open("myfile.txt", "w")
    for i, line in enumerate(f): # Each line is searched for the variables or data points
        a = replace_char(line, "$", "")
        if not a.strip() == "":
            g.write(a)
    g.close()