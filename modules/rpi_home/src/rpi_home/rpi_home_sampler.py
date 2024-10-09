import json
import logging
import time
import os
import paho.mqtt.client as mqtt

from .rpi_home_device import RpiHomeDevice
from .utils import timestamp
from .const import RPI_HOME, RPI_HOME_WWW_DIR, MQTT, HOST, PORT, USERNAME, PASSWORD

logger = logging.getLogger(__name__)

# XXX need to handle a stop command/interrupt

# MQTT -
# subscribe to homeassistant/status - look for an "online" message or "offline"
# either on start, or on reception of an "online" message (is this message automatically sent if we subscribe to the status topic?)
# send a discovery/config message (json), to the topic as "homeassistant/sensor/sensorBedroomT/config":
#
# {
#    "device_class":"temperature",
#    "state_topic":"homeassistant/sensor/sensorBedroom/state",
#    "unit_of_measurement":"°C",
#    "value_template":"{{ value_json.temperature}}",
#    "unique_id":"temp01ae",
#    "device":{
#       "identifiers":[
#           "bedroom01ae"
#       ],
#       "name":"Bedroom",
#       "manufacturer": "Example sensors Ltd.",
#       "model": "K9",
#       "serial_number": "12AE3010545",
#       "hw_version": "1.01a",
#       "sw_version": "2024.1.0",
#       "configuration_url": "https://example.com/sensor_portal/config"
#    }
# }
#
# and a subsequent json message to another topic on the same device "homeassistant/sensor/sensorBedroomH/config":
#
# {
#    "device_class":"humidity",
#    "state_topic":"homeassistant/sensor/sensorBedroom/state",
#    "unit_of_measurement":"%",
#    "value_template":"{{ value_json.humidity}}",
#    "unique_id":"hum01ae",
#    "device":{
#       "identifiers":[
#          "bedroom01ae"
#       ]
#    }
# }
#
# on state updates, we send to the state topic "homeassistant/sensor/sensorBedroom/state"
#
# {
#    "temperature":23.20,
#    "humidity":43.70
# }




class RpiHomeSampler:
    def __init__(self):
        self.rpi_home_device = RpiHomeDevice()

        # set up the sampling parameters
        self.sampling_interval_ms = int(self.rpi_home_device.sampling_interval * 1000)
        self.start_timestamp = timestamp()
        self.counter = 0

        # clamp the starting time stamp to be an absolute multiple of the interval
        self.start_timestamp -= self.start_timestamp % self.sampling_interval_ms

        # try to connect to a mqtt server
        self.mqtt_client = None
        device_settings = self.rpi_home_device.settings
        mqtt_settings = device_settings.get(MQTT, None)
        if mqtt_settings is not None:
            mqtt_client = mqtt.Client(userdata=self)
            mqtt_host = mqtt_settings.get(HOST, None)
            mqtt_port = mqtt_settings.get(PORT, None)
            if mqtt_host is not None and mqtt_port is not None:
                if mqtt_client.connect(host=mqtt_host, port=mqtt_port) == 0:
                    self.mqtt_client = mqtt_client


    def sample(self):
        # get the report
        report = self.rpi_home_device.report()

        # if an mqtt server connection is available
        if self.mqtt_client is not None:
            # XXX TODO - later, include reporting thresholds and only report if any threshold is met
            #            or some minimum time threshold has passed. also interested in whether a
            #            value has met some threshold/boundary value even if the change is small,
            #            perhaps reporting some number of values in sequence after big changes then
            #            stopping until another big change happens?
            self.mqtt_client.publish(RPI_HOME, json.dumps(report))
        else:
            now_file = os.path.join(RPI_HOME_WWW_DIR, "now.json")
            with open(now_file, "w") as f:
                json.dump(report, f)

    def run(self):
        # loop sampling
        while True:
            # compute the next sampling interval, and how long we need to sleep until then (if any)
            self.counter += 1
            target_timestamp = self.start_timestamp + (self.counter * self.sampling_interval_ms)
            now_timestamp = timestamp()
            delta = (target_timestamp - now_timestamp) / 1000
            if delta > 0:
                time.sleep(delta)
            else:
                logger.warning(f"not sleeping (behind target by {delta * 1000} ms)")
            self.sample()
