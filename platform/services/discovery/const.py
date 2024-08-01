RPI_HOME = "rpi_home"

_SVC = "svc"
_SVC_NETWORK_LOCAL = "local."
_SVC_TRANSPORT_TCP = f"_tcp.{_SVC_NETWORK_LOCAL}"
_SVC_PROTOCOL_HTTP = f"_http.{_SVC_TRANSPORT_TCP}"
_SVC_PROTOCOL_HTTP_PORT = 80

_PATH = "path"
_PATH_UTF8 = _PATH.encode("utf-8")
_ZEROCONF = "zeroconf"
