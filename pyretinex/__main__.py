"""Retinex for magnetic resonance images."""

# Part of 'Retinex for MRI' package.
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
from nibabel import load, save, Nifti1Image
from pyretinex.core import multi_scale_retinex_3d
from pyretinex import __version__
import pyretinex.config as cfg


def main():
    """Command line call argument parsing."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'filename',  metavar='path', nargs='+',
        help="Path to nifti file. When a single path is provided applies \
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
    welcome_str = 'Retinex for MRI {}'.format(__version__)
    welcome_decor = '=' * len(welcome_str)
    print('{}\n{}\n{}'.format(welcome_decor, welcome_str, welcome_decor))

    # Determine which alorithm to use
    nr_fileinputs = len(args.filename)
    if nr_fileinputs > 1:
        print('Multiple inputs, using multi-scale retinex with barycenter preservation (MSRBP).')
        id_alg = 'MSRBP'
    else:
        print('Single input, using multi-scale retinex (MSR).')
        id_alg = 'MSR'

    print('Selected scales: {}'.format(cfg.scales))

    # Load nifti
    nii, basename, data = [], [], []
    for i in range(nr_fileinputs):
        nii.append(load(args.filename[i]))
        basename.append(nii[i].get_filename().split(os.extsep, 1)[0])
        data.append(nii[i].get_data())

    # Rearrange
    if nr_fileinputs > 1:  # MSRBP
        data = np.asarray(data)
        data = data.transpose([1, 2, 3, 0])
        inten = np.sum(data, axis=-1)
        bary = data / inten[..., None]
    else:  # MSR
        inten = data[0]

    # Multi-scale retinex
    new_inten = multi_scale_retinex_3d(inten, scales=scales)

    # Scale new data approximately to original dynamic range
    opmin, opmax = np.nanpercentile(inten, [2.5, 97.5])
    npmin, npmax = np.nanpercentile(new_inten, [2.5, 97.5])
    scale_factor = opmax - opmin / (npmax - npmin)
    new_inten *= scale_factor

    # scale identifier
    id_scl = ''
    for s in scales:
        id_scl += '_{}'.format(s)

    # Save corrected image
    print('Saving...')
    for i in range(nr_fileinputs):
        if nr_fileinputs > 1:  # MSRBP
            out_img = bary[..., i] * new_inten
        else:
            out_img = new_inten
        out_name = '{}_{}{}.nii.gz'.format(basename[i], id_alg, id_scl)
        out = Nifti1Image(np.squeeze(out_img), affine=nii[i].affine)
        save(out, out_name)
    print('Finished.')


if __name__ == "__main__":
    main()
