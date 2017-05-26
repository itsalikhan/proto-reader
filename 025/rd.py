from datetime import datetime


# Usually in KITcube tools, we use parameter 'skip-line' to indicate
# where we should start reading. But, I think checking data type gives 
# us a more scalable reader. - NTJ

# Fetch data definitions
SENSOR_DEF = {}


with open('./sensor-definition/jwd.rd.sensors') as f:
    sensor_data = f.readlines()

    for item in sensor_data:
        line_list = item.split("\t")
        SENSOR_DEF[line_list[0].strip()] = line_list[1].strip()


print SENSOR_DEF

with open('./data/rd160715_small') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):

        # rd files does not consist of header
        # We will not perform raw data index here
        
        # Condition to skip the information header
        if line.strip()[0] == "#":
            continue

        # datetime
        current_line = line.split()
        current_date = current_line[0]
        current_time = current_line[2] + "00"
        print datetime.strptime( " ".join([current_date, current_time]), '%y%m%d %H%M%S')
        
        data = current_line[4:]
        # read data only if sensor_definition matches data
        if (len(SENSOR_DEF) == len(data)):
            for k, datum in enumerate(data):
                key = "Class "+ str(k+1)
                print k, ": ", SENSOR_DEF[key], " => ", datum.strip()

        else:
            print("Error: Data structure mismatch between sensor definition and data.")
        
        # I'm only reading one line, hence the 'break'
        # uncomment this to read all 100 lines. - NTJ
        break

