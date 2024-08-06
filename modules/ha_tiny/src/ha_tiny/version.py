import os
import importlib.metadata as metadata

package_name = os.path.basename(os.path.dirname(__file__))
HA_TINY_VERSION = metadata.version(package_name)
