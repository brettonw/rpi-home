RPI_HOME = "rpi_home"
DOMAIN = RPI_HOME
RPI_HOME_ROOT_DIR = "/usr/local/" + RPI_HOME
RPI_HOME_WWW_DIR = "/var/www/html/" + RPI_HOME

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
VALUE = "value"
VALUES = "values"
IP_ADDRESS = "ip_address"
OPERATING_SYSTEM = "operating_system"
UNIT_OF_MEASUREMENT = "unit_of_measurement"
DRIVER = "driver"
CLASS_NAME = "class_name"
CACHE = "cache"

# zeroconf
SVC_NETWORK_LOCAL = "local."
SVC_TRANSPORT_TCP = f"_tcp.{SVC_NETWORK_LOCAL}"
SVC_PROTOCOL_HTTP = f"_http.{SVC_TRANSPORT_TCP}"
RPI_HOME_SERVICE = f"{RPI_HOME}.{SVC_PROTOCOL_HTTP}"
RPI_HOME_SERVICE_PORT = 80
ZEROCONF = "zeroconf"
