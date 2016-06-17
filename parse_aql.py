#!/usr/bin/env python

"""
Parses information from aql and outputs them to one JSON

input:
    stdin: json aql output
        e.g. aql -c "SHOW SETS" -o json | head -n -3
return:
    JSON string
        [[{...], {...}]] - for each server list of stats (e.g for each set)
"""


import sys
import json

data = []

json_in = ''
for l in sys.stdin:
    json_in += l
    if ']' in l:
        # one server collected
        server_stats = []
        for stats in json.loads(json_in):
            server_stats.append(stats)
        json_in = ''
        data.append(server_stats)

print(json.dumps(data))
