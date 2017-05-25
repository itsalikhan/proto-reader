from datetime import datetime
from netCDF4 import Dataset
import pprint

# Usually in KITcube tools, we use parameter 'skip-line' to indicate
# where we should start reading. But, I think checking data type gives 
# us a more scalable reader. - NTJ

# Time is from Date(1904,1,1)
#In [45]: d = date(1904, 1, 1)
#In [46]: timestamp1 = calendar.timegm(d.timetuple())
#Out[47]: -2082844800
time_delta = 2082844800


fh = Dataset("./data/20160720_Save_Benin_CHM070091_1530_000.nc")

with open("./sensor-definition/chm.nc.sensors") as f:
    sensor_data = f.readlines()

    time_since_1904 = fh.variables["time"][:]
    
    #datetime.utcfromtimestamp(1469028605.0)
    
    data = {}
    for i, time_unit in enumerate(time_since_1904):
        time_since_epoch = time_unit - time_delta
        print time_since_epoch, datetime.utcfromtimestamp(time_since_epoch)
        
        data[time_since_epoch] = {}
        # removes the first line
        sensor_data.pop(0)
        for item in sensor_data:
            current_line = item.split("\t")
            print len(current_line), current_line
            if len(current_line) == 4:
                # this section deals with 1D data
                data[time_since_epoch][current_line[2]] = {}
                data[time_since_epoch][current_line[2]]["type"] = "1D"
                data[time_since_epoch][current_line[2]]["dimension"] = ["time"]
                data[time_since_epoch][current_line[2]]["value"] = fh.variables[current_line[1]][i]
            elif len(current_line) == 6:
                # this section deals with 2D data
                tmp_data = []
                data[time_since_epoch][current_line[2]] = {}
                data[time_since_epoch][current_line[2]]["type"] = "2D"
                data[time_since_epoch][current_line[2]]["dimension"] = ["time", current_line[4]]
                val = fh.variables[current_line[1]][i]
                aux_dimension = fh.variables[current_line[4]][:]
                for j, unit in enumerate(val):
                    tmp_data.append({"key":aux_dimension[j], "value": val[j]})
                data[time_since_epoch][current_line[2]]["value"] = tmp_data
            else:
                print("Error: Unknown data structure in sensor definition.")
                continue
        # I'm only reading one line, hence the 'break'
        # uncomment this to read all 100 lines. - NTJ
        break
        
#print data
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data)

