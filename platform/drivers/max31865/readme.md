
See [Adafruit docs for MAX31865](https://learn.adafruit.com/adafruit-max31865-rtd-pt100-amplifier/python-circuitpython)

Example driver:

```
{
    "driver": "max31865", 
    "parameters": {
        "wires": 3, 
        "pt": "PT100", 
        "select_pin": "D5"
    },
    "skip": "resistance"
}
``` 
