
See [Adafruit docs for HTS221](https://learn.adafruit.com/adafruit-hts221-temperature-humidity-sensor)

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
