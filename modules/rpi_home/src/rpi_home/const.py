# capture the initial state of the namespace
_initial_namespace = set(globals().keys())

RPI_HOME = "rpi_home"
RPI_HOME_ROOT_DIR = "/usr/local/" + RPI_HOME
RPI_HOME_WWW_DIR = "/var/www/html/"

# commonly used values
SETTINGS = "settings"
DRIVER_PREFIX = RPI_HOME + "_"
DRIVER_DEFAULT_SENSOR_CLASS_NAME = "Sensor"
DRIVER_DEFAULT_CONTROL_CLASS_NAME = "Control"
TIMESTAMP = "timestamp"
VERSION = "version"
HOST = "host"
SENSORS = "sensors"
CONTROLS = "controls"
NAME = "name"
DISPLAY_NAME = "display_name"
ENTITY_ID = "entity_id"
VALUE = "value"
VALUES = "values"
IP_ADDRESS = "ip_address"
MAC_ADDRESS = "mac_address"
OPERATING_SYSTEM = "operating_system"
SERIAL_NUMBER = "serial_number"
SENSOR_DEVICE_CLASS = "sensor_device_class"
UNIT_OF_MEASUREMENT = "unit_of_measurement"
DRIVER = "driver"
CLASS_NAME = "class_name"
REMAP = "remap"
SKIP = "skip"
PARAMETERS = "parameters"
CACHE = "cache"
SAMPLING_INTERVAL = "sampling_interval"
DEFAULT_SAMPLING_INTERVAL = 10

# capture the current state of the namespace
_current_namespace = set(globals().keys())

DOMAIN = RPI_HOME

# dynamically create __all__ to include all variables defined in this module (not imported)
__all__ = [name for name in (_current_namespace - _initial_namespace)]
