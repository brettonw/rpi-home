import os
import importlib.metadata as metadata

package_name = os.path.basename(os.path.dirname(__file__))
RPI_HOME_VERSION = metadata.version(package_name)
