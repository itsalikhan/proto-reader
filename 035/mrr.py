from datetime import datetime
import time
import calendar


# Usually in KITcube tools, we use parameter 'skip-line' to indicate
# where we should start reading. But, I think checking data type gives 
# us a more scalable reader. - NTJ

# Fetch data definitions
SENSOR_DEF = []
with open('./sensor-definition/mrr.dat.sensors') as f:
    sensor_data = f.readlines()

    # removes the first line 
    sensor_data.pop(0)
    for item in sensor_data:
        SENSOR_DEF.append(item.split("\t"))


counter = 999
lines_per_block = 30

data = {}

with open('./data/int01_160715.dat') as f:
    sensor_data = f.readlines()
    for i, item in enumerate(sensor_data):
        
        # I'm only reading one line, hence the 'break'
        # uncomment this to read all lines. - NTJ
        if counter == 30:
            break

        try:
            current_time = datetime.strptime( item.split()[1], '%Y%m%d%H%M%S')
            timestamp = calendar.timegm(current_time.timetuple())
            start_block = True
            counter = 0
            print current_time, calendar.timegm(current_time.timetuple())
            data[timestamp] = {}
            continue
        except:
            pass
            
        if counter < lines_per_block:
            print item.strip()
            """
            'KCR.CHM.H.CBH.001.AVG': {   'dimension': [   'time',
                                                                    'layer'],
                                                   'type': '2D',
                                                   'value': [   {   'key': 1,
                                                                    'value': 2230},
                                                                {   'key': 2,
                                                                    'value': 5160},
                                                                {   'key': 3,
                                                                    'value': -1}]},            
            """
            
            counter += 1
 
