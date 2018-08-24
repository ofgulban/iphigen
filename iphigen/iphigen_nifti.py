"""Python implementation of retinex image enhancement algorithm."""

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
import numpy as np
import nibabel as nb
from iphigen import core, utils
from iphigen.ui import user_interface, display_welcome_message
import iphigen.config as cfg


def main():
    """Process for nifti images."""
    user_interface()
    display_welcome_message()
    print('Selected scales:\n  {}'.format(cfg.scales_nifti))

    # Load data
    data, affine, dirname, basename, ext = [], [], [], [], []
    nr_fileinputs = len(cfg.filename)
    print('Selected file(s):')
    for i in range(nr_fileinputs):
        nii = nb.load(cfg.filename[i])
        affine.append(nii.affine)
        parses = utils.parse_filepath(cfg.filename[i])
        data.append(np.squeeze(nii.get_data()))
        print('  Name: {}'.format(cfg.filename[i]))
        print('  Dimensions: {}'.format(data[i].shape))
        dirname.append(parses[0])
        basename.append(parses[1])
        ext.append(parses[2])

    # Reorganize data
    data = np.asarray(data)
    data = data.transpose([1, 2, 3, 0])
    # Compute intensity
    inten = np.sum(data, axis=-1)
    # Compute barycentic coordinates (equivalent to intensity for 0-simplex)
    bary = data / inten[..., None]

    # Appy multi-scale retinex on intensity
    new_inten = core.multi_scale_retinex(inten, scales=cfg.scales_nifti)
    # Scale back to the approximage original intensity range
    new_inten = core.scale_approx(new_inten, inten)

    #  Balance components if desired
    id_bal = ''
    if cfg.intensity_balance:
        print('Applying intensity balance...')
        new_inten = utils.truncate_and_scale(
            new_inten, percMin=2.5, percMax=97.5, zeroTo=255*data.shape[-1])
        id_bal = id_bal + '_IB'
    if cfg.color_balance:
        print('Applying color balance...')
        bary = core.simplex_color_balance(bary)
        id_bal = id_bal + '_CB'

    # Insert back the processed intensity image
    new_data = bary * new_inten[..., None]

    print('Saving output(s)...')
    id_scl = utils.prepare_scale_suffix(cfg.scales_nifti)
    for i in range(nr_fileinputs):
        # Generate output path
        out_name = '{}_MSRBP{}{}'.format(basename[i], id_scl, id_bal)
        out_basepath = os.path.join(dirname[i], out_name)
        out_path = out_basepath + os.extsep + ext[i]
        # Create nifti image and save
        img = nb.Nifti1Image(new_data[..., i], affine=affine[i])
        nb.save(img, out_path)
        print('  {} is saved.'.format(out_path))
    print('Finished.')


if __name__ == "__main__":
    main()
