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
import cv2
import numpy as np
from pyretinex import core, utils
from pyretinex.ui import user_interface, display_welcome_message
import pyretinex.config as cfg


def main():
    """Pyretinex for 2D images."""
    user_interface()
    display_welcome_message()

    # Load data
    data, dirname, basename, ext = [], [], [], []
    nr_fileinputs = len(cfg.filename)
    print('Selected file(s):')
    for i in range(nr_fileinputs):
        data.append(np.squeeze(cv2.imread(cfg.filename[i])))
        parses = utils.parse_filepath(cfg.filename[i])
        print('  Name: {}'.format(cfg.filename[i]))
        print('  Dimensions: {}'.format(data[i].shape))
        dirname.append(parses[0])
        basename.append(parses[1])
        ext.append(parses[2])

    # Reorganize data
    data = np.asarray(data, dtype=float)
    data = data.transpose([1, 2, 3, 0])
    data = np.squeeze(data)
    # Compute intensity
    inten = np.sum(data, axis=-1)
    # Compute barycentic coordinates (equivalent to intensity for 0-simplex)
    bary = data / inten[..., None]

    if cfg.no_retinex:
        id_ret = ''
    else:
        print('Selected retinex scales:\n  {}'.format(cfg.scales))
        id_ret = '_MSRBP' + utils.prepare_scale_suffix(cfg.scales)
        orig_inten = np.copy(inten)
        # Appy multi-scale retinex on intensity
        inten = core.multi_scale_retinex(inten, scales=cfg.scales)
        # Scale back to the approximage original intensity range
        inten = core.scale_approx(inten, orig_inten)

    #  Balance components if desired
    id_bal = ''
    if cfg.intensity_balance:
        print('Applying intensity balance...')
        inten = utils.truncate_and_scale(inten, percMin=1, percMax=99,
                                         zeroTo=255*data.shape[-1])
        id_bal = id_bal + '_IB'
    if cfg.color_balance:
        print('Applying color balance...')
        bary = core.simplex_color_balance(bary)
        id_bal = id_bal + '_CB'

    # Insert back the processed intensity image
    new_data = bary * inten[..., None]

    print('Saving output(s)...')
    for i in range(nr_fileinputs):
        # Generate output path
        out_name = '{}{}{}'.format(basename[i], id_ret, id_bal)
        out_basepath = os.path.join(dirname[i], out_name)
        out_path = out_basepath + os.extsep + ext[i]
        # Save 2D image
        cv2.imwrite(out_path, new_data)
        print('  {} is saved.'.format(out_path))
    print('Finished.')


if __name__ == "__main__":
    main()
