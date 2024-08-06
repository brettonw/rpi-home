# Host

## DESCRIPTION
This is the basic host driver for rpi-home sensors. it delivers basic health characteristics of the host raspberry pi.

## PARAMETERS
### remap
`remap` is available for all rpi-home sensors to allow the `display_name` and/or `entity_id` of any of the outputs to be mapped to another string.

EXAMPLES:

```
{
    "driver": "host", 
    "remap": {
        "display_name": {"CPU Usage": "System Usage"}, 
        "entity_id": {"cpu_usage", "system_usage"}
    }
}
```

### skip
`skip` is available for all rpi-home sensors to suppress reporting of a particular sensor. It is a single entity id or a list of entity ids to skip after `remap`, and does not suppress generation of the sensor report.

EXAMPLES:

```
{"driver": "host", "skip": "swap_usage"}
```

It probably wouldn't make much sense to remap a name that you wanted to skip reporting for, but it would work:
```
{
    "driver": "host", 
    "remap": {
        "display_name": {"CPU Usage": "System Usage"}, 
        "entity_id": {"cpu_usage", "system_usage"}
    },
    "skip": ["swap_usage", "system_usage", "cpu_temperature"]
}
```
