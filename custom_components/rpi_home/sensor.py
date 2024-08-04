import logging
from typing import Any

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorDeviceClass, SensorEntity, SensorStateClass
from rpi_home import NAME, SENSOR_DEVICE_CLASS, UNIT_OF_MEASUREMENT, SERIAL_NUMBER
logger = logging.getLogger(__name__)


class RpiHomeSensor(SensorEntity):
    def __init__(self, host: dict[str, Any], record: dict[str, Any]):
        # logger.debug(f"Adding '{sensor_type}" + ("" if sensor_subtype == "" else f"-{sensor_subtype}") + f" sensor from host: ({config[CONF_HOST]})")
        (host_name, host_serial_number) = (host[NAME], host[SERIAL_NUMBER])
        (sensor_name, sensor_device_class, sensor_unit_of_measurement) = (record[NAME], record[SENSOR_DEVICE_CLASS], record[UNIT_OF_MEASUREMENT])

        # we generally assume names are unique within devices

        # if there is a display name but no id, we make an id by eliminating non alpha chars...
        self._attr_name = f"{host_name} {sensor_name}"
        self._attr_unique_id = self._attr_name.replace(" ", "_").lower()

        self._attr_native_unit_of_measurement = unit_of_measurement if unit_of_measurement != "" else None
        self._attr_device_class = RpiSensorType.ha_device_classes.get(sensor_type, sensor_type)
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._sensor_type = sensor_type
        self._sensor_subtype = sensor_subtype
        self._record = record

        self._host = config[CONF_HOST]
        self.update()

    def update(self):
        record = RpiSensor.api(self._host, self._record, DATA_REFRESH_INTERVAL_MS)
        if (record is not None) and (self._sensor_type in record):
            if self._sensor_subtype == "":
                self._attr_native_value = record[self._sensor_type]
            else:
                self._attr_native_value = record[self._sensor_type][self._sensor_subtype]
        self._record = record
