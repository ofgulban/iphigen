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
import numpy as np
from pyretinex.core import multi_scale_retinex
from pyretinex.utils import load_data, save_data
from pyretinex.ui import user_interface, display_welcome_message
import pyretinex.config as cfg


def main():
    """Pyretinex for 3D MRI data."""
    user_interface()
    display_welcome_message()
    print('Selected scales: {}'.format(cfg.scales))

    # Load data
    data, dirname, basename, ext, filename = [], [], [], [], []
    nr_fileinputs = len(cfg.filename)
    for i in range(nr_fileinputs):
        iData, iDirname, iBasename, iExt = load_data(cfg.filename[i])
        filename.append(cfg.filename[i])
        data.append(iData)
        dirname.append(iDirname)
        basename.append(iBasename)
        ext.append(iExt)
        print('  Name: {}'.format(iBasename))
        print('  Extension: {}'.format(iExt))
        print('  Dimensions: {}'.format(iData.shape))

    # Rearrange in case of multiple inputs
    if nr_fileinputs > 1:
        data = np.asarray(data)
        data = data.transpose([1, 2, 3, 0])
    else:
        data = data[0]
    dims = data.shape

    # Single channel image barycenter does not exists (0-simplex)
    if len(dims) == 4 and dims[-1] > 1:
        inten = np.sum(data, axis=-1)
        bary = data / inten[..., None]
    else:
        inten = data

    # Multi-scale retinex
    new_inten = multi_scale_retinex(inten, scales=cfg.scales)

    # Scale new data approximately to original dynamic range
    # TODO: replace percentile with gradient based percentile
    opmin, opmax = np.nanpercentile(inten, [2.5, 97.5])
    npmin, npmax = np.nanpercentile(new_inten, [2.5, 97.5])
    scale_factor = opmax - opmin / (npmax - npmin)
    new_inten *= scale_factor

    # identifiers to use as suffixes
    id_alg = 'MSRBP'
    id_scl = ''
    for s in cfg.scales:
        id_scl += '_{}'.format(s)

    # Save output image
    for i in range(nr_fileinputs):

        # Single channel image barycenter does not exists (0-simplex)
        if nr_fileinputs > 1:
            out_data = bary[..., i] * new_inten
        else:
            out_data = new_inten

        # Generate output path
        out_name = '{}_{}{}'.format(basename[i], id_alg, id_scl)
        out_basepath = os.path.join(dirname[i], out_name)

        save_data(out_data, out_basepath, ext[i],
                  original_filepath=filename[i])

    print('Finished.')


if __name__ == "__main__":
    main()
