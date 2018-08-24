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
    for f in cfg.filename:
        data = cv2.imread(f)
        dirname, basename, ext = utils.parse_filepath(f)
        if cfg.out_dir:
            dirname = cfg.out_dir
        print('Selected file:')
        print('  Name: {}'.format(f))
        print('  Dimensions: {}'.format(data.shape))

        data = np.asarray(data, dtype=float)
        # Compute intensity
        inten = np.sum(data, axis=-1)
        # Compute barycentic coordinates
        bary = data / inten[..., None]

        id_bal = ''
        if cfg.intensity_balance:
            print('Applying intensity balance...')
            inten = utils.truncate_and_scale(inten, percMin=1, percMax=99,
                                             zeroTo=255*data.shape[-1])
            id_bal = id_bal + '_IB'
            data = bary * inten[..., None]
            # Update barycentic coordinates
            bary = data / inten[..., None]

        if cfg.no_retinex:
            id_ret = ''
        else:
            print('Selected retinex scales:\n  {}'.format(cfg.scales))
            id_ret = '_MSRBP' + utils.prepare_scale_suffix(cfg.scales)
            # Appy multi-scale retinex on intensity
            new_inten = core.multi_scale_retinex(inten, scales=cfg.scales)
            # Scale back to the approximage original intensity range
            inten = core.scale_approx(new_inten, inten)

        if cfg.color_balance:
            print('Applying color balance...')
            bary = core.simplex_color_balance(bary)
            id_bal = id_bal + '_CB'

        # Insert back the processed intensity image
        new_data = bary * inten[..., None]

        print('Saving output(s)...')
        # Generate output path
        out_name = '{}{}{}'.format(basename, id_ret, id_bal)
        out_basepath = os.path.join(dirname, out_name)
        out_path = out_basepath + os.extsep + ext
        # Save 2D image
        cv2.imwrite(out_path, new_data)
        print('  {} is saved.'.format(out_path))
    print('Finished.')


if __name__ == "__main__":
    main()
