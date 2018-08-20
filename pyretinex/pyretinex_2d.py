"""Python implementation of retinex image enhancement algorithm."""

# Part of Pyretinex package.
# Copyright (C) 2018  Omer Faruk Gulban
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import os
import argparse
import numpy as np
import cv2
from pyretinex.core import multi_scale_retinex
from pyretinex import __version__
from pyretinex.utils import truncate_and_scale
import pyretinex.config as cfg


def main():
    """Command line call argument parsing."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'filename',  metavar='path',
        help="Path to image. When a single path is provided applies \
        multi-scale retinex (MSR). Otherwise switches to multi-scale retinex \
        with barycenter preservation (MSRBP)."
        )
    parser.add_argument(
        '--scales', nargs='+', type=int, required=False,
        metavar=' '.join(str(e) for e in cfg.scales),
        help="Retinex scales."
        )

    args = parser.parse_args()
    if args.scales:
        scales = args.scales
    else:
        scales = cfg.scales

    # Welcome message
    welcome_str = 'PyRetinex {}'.format(__version__)
    welcome_decor = '=' * len(welcome_str)
    print('{}\n{}\n{}'.format(welcome_decor, welcome_str, welcome_decor))

    # Determine which alorithm to use
    print('2D mode, using multi-scale retinex with barycenter preservation (MSRBP).')
    id_alg = 'MSRBP'

    print('Selected scales: {}'.format(scales))

    # Load nifti
    basename, extention = args.filename[0].split(os.extsep, 1)
    data = cv2.imread(args.filename[0])

    inten = np.sum(data, axis=-1)
    bary = data / inten[..., None]

    # Multi-scale retinex
    new_inten = multi_scale_retinex(inten, scales=scales)

    # Scale new data approximately to original dynamic range
    opmin, opmax = np.nanpercentile(inten, [2.5, 97.5])
    npmin, npmax = np.nanpercentile(new_inten, [2.5, 97.5])
    scale_factor = opmax - opmin / (npmax - npmin)
    new_inten *= scale_factor

    # Corrected image
    out_img = bary * new_inten[..., None]
    out_img = np.nan_to_num(out_img)

    # Scale each channel for uint8 precision with simplest color balance
    # TODO: Replace this with simplex color balance
    for i in range(3):
        out_img[..., i] = truncate_and_scale(out_img[..., i],
                                             percMin=2.5, percMax=97.5)

    print('Saving...')
    id_scl = ''  # scale identifier
    for s in scales:
        id_scl += '_{}'.format(s)
    out_name = '{}_{}{}.{}'.format(basename, id_alg, id_scl, extention)
    cv2.imwrite(out_name, out_img)
    print('Finished.')


if __name__ == "__main__":
    main()
