import os
import importlib.metadata as metadata

_package_name = os.path.basename(os.path.dirname(__file__))
DRIVER_VERSION = metadata.version(_package_name)
