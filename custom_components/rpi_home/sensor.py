import logging
from typing import Any

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorDeviceClass, SensorEntity, SensorStateClass
from rpi_home import NAME, DISPLAY_NAME, ENTITY_ID, SENSOR_DEVICE_CLASS, UNIT_OF_MEASUREMENT, SERIAL_NUMBER
logger = logging.getLogger(__name__)


class RpiHomeSensor(SensorEntity):
    def __init__(self, host: dict[str, Any], record: dict[str, Any]):
        # logger.debug(f"Adding '{sensor_type}" + ("" if sensor_subtype == "" else f"-{sensor_subtype}") + f" sensor from host: ({config[CONF_HOST]})")
        (host_name, host_display_name, host_serial_number) = (host[NAME], host[DISPLAY_NAME], host[SERIAL_NUMBER])
        (sensor_display_name, sensor_entity_id, sensor_device_class, sensor_unit_of_measurement) = (record[DISPLAY_NAME], record[ENTITY_ID], record[SENSOR_DEVICE_CLASS], record.get(UNIT_OF_MEASUREMENT, None))

        self._attr_name = f"{host_display_name} {sensor_display_name}"
        self._attr_unique_id = self._attr_name.replace(" ", "_").lower()

        self._attr_native_unit_of_measurement = sensor_unit_of_measurement
        self._attr_device_class = sensor_device_class
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def update(self):
        record = RpiSensor.api(self._host, self._record, DATA_REFRESH_INTERVAL_MS)
        if (record is not None) and (self._sensor_type in record):
            if self._sensor_subtype == "":
                self._attr_native_value = record[self._sensor_type]
            else:
                self._attr_native_value = record[self._sensor_type][self._sensor_subtype]
        self._record = record
