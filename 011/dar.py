from datetime import datetime


# Usually in KITcube tools, we use parameter 'skip-line' to indicate
# where we should start reading. But, I think checking data type gives 
# us a more scalable reader. - NTJ

# Fetch data definitions
SENSOR_DEF = {}


with open('./sensor-definition/EBM_DAR.sensors') as f:
    sensor_data = f.readlines()

    for item in sensor_data:
        line_list = item.split("\t")
        SENSOR_DEF[line_list[0].strip()] = line_list[1].strip()


with open('./data/EBM1_DAR_small.dat') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        
        # Assigning Index to read specific raw data columns
        if i == 1:
            # get column names after 'mod'
            COLUMN = line.split()
        
        # Condition to skip the information header
        try:
            datetime.strptime(str(line.split(',')[0]), '"%Y-%m-%d %H:%M:%S"')
        except ValueError, e:
            continue
        
        
        current_line = line.split(",")


        # read data only if sensor_definition matches data
        if (len(SENSOR_DEF) == len(current_line)):
            for k, datum in enumerate(current_line):
                print k, ": ", SENSOR_DEF[k][2], " => ", datum.strip()

        else:
            print("Error: Data structure mismatch between sensor definition and data.")

        # I'm only reading one line, hence the 'break'
        # uncomment this to read all 100 lines. - NTJ
        break
