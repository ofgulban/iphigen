"""Multi scale retinex."""

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
import time
import numpy as np
from scipy.ndimage import gaussian_filter
np.seterr(divide='ignore', invalid='ignore')


def multi_scale_retinex(image, scales=None, verbose=True):
    """Multi scale retinex (MSR).

    Parameters
    ----------
    image : 2d or 3d numpy array

    scales : list
        Standard deviations for Gaussian kernels. For futher
        information see [1]. More or less than 3 values can be given.
        Disscussion of how to determine/optimize the scale values can
        be found in [2].

    Returns
    -------
    msr: 3d numpy array
        Corrected image.

    References
    ----------
    [1] https://github.com/scipy/scipy/blob/v0.16.1/scipy/ndimage/filters.py#L251

    [2] Jobson, D. J., Rahman, Z. U., & Woodell, G. A. (1997).
    A multiscale retinex for bridging the gap between color images and
    the human observation of scenes. IEEE Transactions on Image
    Processing, 6(7), 965-976. DOI: 10.1109/83.597272

    """
    if scales is None:  # default parameters
        scales = [1, 5, 10]

    start = time.time()
    if verbose:
        print('Applying multi-scale retinex...')
    scales = np.array(scales)  # sigma values
    msr = np.zeros(image.shape + (scales.size,))

    for i, sigma in enumerate(scales):
        if verbose:
            print('  .')
        temp = gaussian_filter(image, sigma, mode="constant", cval=0.0)
        msr[..., i] = np.log(image + 1) - np.log(temp + 1)
    temp = None

    # remove nans
    msr = np.nan_to_num(msr)
    # average
    msr = np.mean(msr, axis=-1)
    msr = np.nan_to_num(msr)
    # return from logarithmic space
    msr = np.exp(msr - 1)

    duration = time.time() - start
    print('Multi-scale retinex computed in {0:.1f} seconds.'.format(duration))

    return msr
