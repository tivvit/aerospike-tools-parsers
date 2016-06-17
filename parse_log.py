#!/usr/bin/env python

"""
parses Aerospike log (device part) stored at the default place
- keeps processed log position
- converts time to unix timestamp
return:
    JSON string
"""

import os
import json
from datetime import datetime

path = "/var/log/aerospike/aerospike.log"
pos_file = "log.pos"
stats = []

pos = 0
try:
    with open(pos_file, "r") as w:
        pos = int(w.read())
except Exception:
    pass

# log was rotated
if pos > os.path.getsize(path):
    pos = 0

with open(path, "r") as f:
    f.seek(pos)
    for line in f:
        if "device" in line:
            data = {}
            # data example
            # Jun 16 2016 13:36:14 GMT: INFO (drv_ssd): (drv_ssd.c::2088) device /www/aerospike/data/er.dat: used 1013766400, contig-free 15169M (15169 wblocks), swb-free 0, w-q 0 w-tot 0 (0.0/s), defrag-q 0 defrag-tot 0 (0.0/s) defrag-w-tot 0 (0.0/s)
            parts = line.split()
            data["timestamp"] = (datetime.strptime(" ".join(parts[:5])[:-1],
                                                   "%b %d %Y %H:%M:%S %Z") -
                                 datetime(1970, 1, 1)).total_seconds()
            data["device"] = parts[9][:-1]
            data["used_B"] = int(parts[11][:-1])
            data["contig-free_MB"] = int(parts[13][:-1])
            data["contig-free_wblocks"] = int(parts[14][1:])
            data["swb-free"] = int(parts[17][:-1])
            data["w-q"] = int(parts[19])
            data["w-tot"] = int(parts[21])
            data["w-tot_speed_s"] = float(parts[22][1:-4])
            data["defrag-q"] = int(parts[24])
            data["defrag-tot"] = int(parts[26])
            data["defrag-tot_speed_s"] = float(parts[27][1:-4])
            data["defrag-w-tot"] = int(parts[29])
            data["defrag-w-tot_speed_s"] = float(parts[30][1:-4])

            stats.append(data)

    # write last processed position
    with open(pos_file, "w") as w:
        w.write(str(f.tell()))

print(json.dumps(stats))
