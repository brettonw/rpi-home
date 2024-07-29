import os
import importlib.metadata as metadata

package_name = os.path.basename(os.path.dirname(__file__))
DRIVER_VERSION = metadata.version(package_name)
