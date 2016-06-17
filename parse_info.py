#!/usr/bin/env python

"""
Parses asinfo output into JSON


input:
    stdin: line separated asinfo output
        e.g. asinfo v 'statistics' -l
return:
    JSON string
        [{...}, {...}]
"""

import sys
import json


def parse_entry(entry):
    """
    Parse one entry and stores it to provided dict
    - converts value to int if possible

    :type entry: str
    :rtype: dict
    """
    k, v = entry.split('=')
    try:
        v = int(v)
    except Exception:
        pass
    return {k: v}


data = []
stats = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    # some fields are nested - e.g. sets
    if ':' in line and ',' not in line:
        stats = {}
        for entry in line.split(':'):
            stats.update(parse_entry(entry))
        data.append(stats)
    else:
        stats.update(parse_entry(line))
# store stats for non-nested fields
if not data:
    data.append(stats)

print(json.dumps(data))
