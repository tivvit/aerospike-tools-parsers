#!/usr/bin/env python

"""
parses asmonitor output and returns it as JSON
- adds sourceIp, port fields

input:
    stdin: asmonitor section output
        e.g. asmonitor -e stat
return:
    JSON string
        [{...},{...}] dict of stats for each server
"""

import sys
import json


def parse_address(server_name):
    """
    Parses the server ip and port

    :param server_name: server name in format 10.0.0.1:3000
    :type server_name: str
    :return: dict with source IP and port
    :rtype: dict
    """
    addr = server_name.split(':')
    return {
        "sourceIp": addr[0],
        "port": addr[1]
    }


data = []
server_stat = {}
server_name = ""

for line in sys.stdin:
    line = line.strip()
    if "====" in line:
        if server_name:
            server_stat.update(server_name)
            data.append(server_stat)
        line = line.replace("====", "")
        line = line.replace("'", "")
        server_name = line
        server_stat = {}
        continue

    k, v = line.split()
    try:
        v = int(v)
    except Exception:
        pass
    server_stat[k] = v

# add last server result
server_stat.update(parse_address(server_name))
data.append(server_stat)

print(json.dumps(data))
