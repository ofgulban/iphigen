"""RGB image processing with retinex and balance methods."""

# Part of Iphigen package.
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
from iphigen import core, utils
from iphigen.ui import user_interface, display_welcome_message
import iphigen.config as cfg


def main():
    """Iphigen processes for 2D images."""
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

        suf = ''  # suffix
        if cfg.intensity_balance:
            print('Applying intensity balance...')
            print('  Percentiles: {}'.format(cfg.int_bal_perc))
            suf = suf + '_IB'
            inten = utils.truncate_and_scale(
                inten, pmin=cfg.int_bal_perc[0], pmax=cfg.int_bal_perc[1],
                zero_to=255*data.shape[-1])
            data = bary * inten[..., None]
            # Update barycentic coordinates
            bary = data / inten[..., None]

        if cfg.retinex:
            print('Applying multi-scale retinex with color preservation (MSRCP)...')
            print('  Selected retinex scales: {}'.format(cfg.scales))
            suf = suf + '_MSRCP' + utils.prepare_scale_suffix(cfg.scales)
            new_inten = core.multi_scale_retinex(inten, scales=cfg.scales)
            # Scale back to the approximage original intensity range
            inten = core.scale_approx(new_inten, inten)

        if cfg.simplex_color_balance:
            print('Applying simplex color balance...')
            print('  Centering: {}'.format(cfg.simplex_center))
            print('  Standardize: {}'.format(cfg.simplex_standardize))
            suf = suf + '_SimplexCB'
            bary = core.simplex_color_balance(
                bary, center=cfg.simplex_center,
                standardize=cfg.simplex_standardize)

        # Insert back the processed intensity image
        data = bary * inten[..., None]

        if cfg.simplest_color_balance:
            print('Applying simplest color balance...')
            print('  Percentiles: {}'.format(cfg.int_bal_perc))
            suf = suf + '_SimplestCB'
            data = core.simplest_color_balance(
                data, pmin=cfg.simplest_perc[0], pmax=cfg.simplest_perc[1])

        # Check at least one operation is selected before saving anything
        if sum([cfg.retinex, cfg.intensity_balance, cfg.simplex_color_balance,
                cfg.simplest_color_balance]) > 0:
            print('Saving output...')
            out_basepath = os.path.join(dirname, '{}{}'.format(basename, suf))
            out_path = out_basepath + os.extsep + ext
            cv2.imwrite(out_path, data)
            print('  {} is saved.\n'.format(out_path))
        else:
            print('No operation selected, not saving anything.')
    print('Finished.')


if __name__ == "__main__":
    main()
