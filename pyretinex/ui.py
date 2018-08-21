"""Collection of simple, handy functions."""

import argparse
import pyretinex.config as cfg
from pyretinex import __package__, __version__


def display_welcome_message(package=__package__, version=__version__):
    """Print program name and version."""
    welcome_str = '{} {}'.format(package, version)
    welcome_decor = '=' * len(welcome_str)
    print('{}\n{}\n{}'.format(welcome_decor, welcome_str, welcome_decor))


def user_interface():
    """Commandline interface."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'filename',  metavar='path', nargs='+',
        help="Path to image. When a single path is provided applies \
        multi-scale retinex (MSR). Otherwise switches to multi-scale retinex \
        with barycenter preservation (MSRBP)."
        )
    parser.add_argument(
        '--scales', nargs='+', type=int, required=False,
        metavar=' '.join(str(e) for e in cfg.scales), default=cfg.scales,
        help="Standard deviations for Gaussian kernels. More or less than 3 \
        values can be given. Disscussion of how to determine/optimize the \
        scale values can be found in Jobson, Rahman, Woodell (1997)"
        )
    parser.add_argument(
        "--color_balance", action='store_true',
        help="Apply simplest color balance at the last step (TODO: add ref)."
        )

    args = parser.parse_args()
    cfg.filename = args.filename
    cfg.scales = args.scales
    cfg.mode = args.mode
    cfg.color_balance = args.color_balance