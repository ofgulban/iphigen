"""Collection of simple, handy functions."""

import os
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
        '--out_dir', type=str, metavar='path', required=False,
        default=cfg.out_dir,
        help="Absolute path of output directory. If not provided, processed \
        images will be saved in the input image path."
        )
    parser.add_argument(
        '--scales', nargs='+', type=int, required=False,
        metavar=' '.join(str(e) for e in cfg.scales), default=cfg.scales,
        help="Standard deviations for Gaussian kernels. More or less than 3 \
        values can be given. Disscussion of how to determine/optimize the \
        scale values can be found in Jobson, Rahman, Woodell (1997)"
        )
    parser.add_argument(
        "--intensity_balance", action='store_true',
        help="Experimental, work in progress."
        )
    parser.add_argument(
        "--color_balance", action='store_true',
        help="Experimental, work in progress."
        )
    parser.add_argument(
        "--no_retinex", action='store_true',
        help="Do not perform retinex image enhancement. Useful for diagnosis."
        )

    args = parser.parse_args()
    cfg.filename = args.filename
    cfg.out_dir = args.out_dir
    cfg.scales = args.scales
    cfg.intensity_balance = args.intensity_balance
    cfg.color_balance = args.color_balance
    cfg.no_retinex = args.no_retinex

    for f in cfg.filename:
        if os.path.isfile(f):
            pass
        else:
            raise ValueError('{} cannot be read.'.format(f))

    if cfg.out_dir:
        if os.path.isdir(cfg.out_dir):
            pass
        else:
            os.mkdir(cfg.out_dir)
