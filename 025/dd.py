from datetime import datetime


# Usually in KITcube tools, we use parameter 'skip-line' to indicate
# where we should start reading. But, I think checking data type gives 
# us a more scalable reader. - NTJ

# Fetch data definitions
SENSOR_DEF = {}


with open('./sensor-definition/jwd.dd.sensors') as f:
    sensor_data = f.readlines()

    for item in sensor_data:
        line_list = item.split("\t")
        SENSOR_DEF[line_list[0].strip()] = line_list[1].strip()


with open('./data/dd160715_small') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):

        # Assigning Index to read specific raw data columns
        if i == 0:
            # get column names after 'mod'
            COLUMN = line.split()[5:]

        # Condition to skip the information header
        if line.strip()[0] == "#":
            continue

        # datetime
        current_line = line.split()
        current_date = current_line[0]
        current_time = current_line[2] + "00"
        print datetime.strptime( " ".join([current_date, current_time]), '%y%m%d %H%M%S')

        # Store data based on SENSOR_DEF      
        data = current_line[4:]
        for k, datum in enumerate(data):
            if COLUMN[k] in SENSOR_DEF:
                print k, ": ", SENSOR_DEF[COLUMN[k]], " => ", datum.strip()

        # I'm only reading one line, hence the 'break'
        # uncomment this to read all 100 lines. - NTJ
        break

