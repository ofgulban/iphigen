"""For having the version."""

import pkg_resources

__version__ = pkg_resources.require("retinex_for_mri")[0].version
