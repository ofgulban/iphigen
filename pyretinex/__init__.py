"""For having the version."""

import pkg_resources

__version__ = pkg_resources.require("pyretinex")[0].version
