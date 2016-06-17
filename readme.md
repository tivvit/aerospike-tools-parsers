# Aerospike Tools Parsers - Useful for logging statistics (to Elasticsearch)

![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)

Set of scripts which transforms Aerospike's monitoring outputs to JSON

- Those JSONs may be sent for example to Elasticsearch (with curl)

## Hints for Aerospike logging

- `asinfo` is the ideal tool for automated logging
  - It shows statistics for one node
- `asmonitor` is great tool for reviewing the state of the cluster
  - It shows statistics for whole cluster
- `aql` is more suitable for viewing data, but it has handy JSON output

## Examples

### Asinfo

```shell
asinfo v 'statistics' -l | python parse_info.py
```

#### Monitor Namespaces
```shell
for n in $(asinfo -v 'namespaces' -l); do (echo "namespace=$n"; asinfo -v "namespace/$n" -l) | python parse_info.py; done
```

### Logfile
This script parses Aerospike's log file, searches drive info and keeps the latest position
- Useful for monitoring drive speed (write, defrag queues)
- ATTENTION this script is not stateless - two calls will not return same results

```shell
python parse_log.py
```

### AQL
```shell
aql -c "SHOW SETS" -o json | head -n -3 | python parse_aql.py
```

### Asmonitor
```shell
asmonitor -e stat | python parse_monitor.py
```

## Todo
* [ ] tests (Install and run cluster, install Aerospike-tools and then check outputs)

## License

&copy; 2016 [tivvit.cz](http://tivvit.cz)

Released under MIT license
