"""Core functions of pyretinex."""

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
import compoda.core as coda
from scipy.ndimage import gaussian_filter
from pyretinex.utils import truncate_and_scale
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
    [1] https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter.html

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
            print('  Processing scale {} (sigma={})...'.format(i+1, sigma))
        temp = gaussian_filter(image, sigma, mode="reflect")
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
    print('  Took {0:.1f} seconds.'.format(duration))

    return msr


def scale_approx(new_image, old_image):
    """Scale new data approximately to original dynamic range.

    TODO: replace percentile with gradient based percentile
    """
    opmin, opmax = np.nanpercentile(old_image, [2.5, 97.5])
    npmin, npmax = np.nanpercentile(new_image, [2.5, 97.5])
    print('old:{} {}'.format(opmin, opmax))
    print('new:{} {}'.format(npmin, npmax))
    scale_factor = opmax - opmin / (npmax - npmin)
    new_image *= scale_factor
    return new_image


def simplest_color_balance(image, pmin=2.5, pmax=97.5):
    """Simplest color balance.

    Parameters
    ----------
    image: ndim numpy array
        Last dimension should contain channels (eg. RGB)
    pmin: float
    pmax: float

    Reference
    ---------
    Limare, N., Lisani, J., Morel, J., Petro, A. B., & Sbert, C. (2011).
    Simplest Color Balance. Image Processing On Line, 1(1), 125-133.
    http://doi.org/10.5201/ipol.2011.llmps-scb

    """
    dims = image.shape
    for d in range(dims[-1]):
        image[..., d] = truncate_and_scale(image[..., d],
                                           percMin=pmin, percMax=pmax)
    return image


def simplex_color_balance(bary, center=True, standardize=False,
                          trunc_max=False):
    """Compositional data based method for color balance.

    Parameters
    ----------
    bary: numpy.ndarray
        Barycentric coordinates. Sum of all channels should add up to 1
        (closed).

    Returns
    -------
    bary: numpy.ndarray
        Processed composition.

    """
    dims = bary.shape
    bary = bary.reshape([np.prod(dims[:-1]), dims[-1]])
    bary = np.nan_to_num(bary)

    # Do not consider values <= 0
    mask = np.prod(bary, axis=-1)
    mask = mask > 0
    temp = bary[mask]

    # Interpretation of centering: Compositions cover the simplex space more
    # balanced across components. Similar to de-mean data.
    if center:
        sample_center = coda.sample_center(temp)
        temp2 = np.full(temp.shape, sample_center)
        temp = coda.perturb(temp, temp2**-1.)
        temp2 = None

    # Interpretation of standardization: Centered compositions cover the
    # dynamic range of simplex space more.
    if standardize:  # Standardize
        totvar = coda.sample_total_variance(temp, sample_center)
        temp = coda.power(temp, np.power(totvar, -1./2.))

    # Interpretation of max truncation: Pull the exterme compositions to
    # threshold distance by using scaling. Scaling factor is determined for
    # each outlier composition to pull more extreme compositions more strongly.
    if trunc_max:
        # Use Aitchison norm and powering to truncate extreme compositions
        anorm = coda.aitchison_norm(temp)
        anorm_thr_min, anorm_thr_max = np.percentile(anorm, [1., 99.])
        # Max truncate
        idx_trunc = anorm > anorm_thr_max
        truncation_power = anorm[idx_trunc] / anorm_thr_max
        correction = np.ones(anorm.shape)
        correction[idx_trunc] = truncation_power
        temp = coda.power(temp, correction[:, None])
        # min truncate
        idx_trunc = anorm < anorm_thr_min
        truncation_power = anorm[idx_trunc] / anorm_thr_min
        correction = np.ones(anorm.shape)
        correction[idx_trunc] = truncation_power
        temp = coda.power(temp, correction[:, None])
    # TODO: Implement this similar to truncate and scpe function but for
    # simplex space. Proportion of dynamic range to the distance of between
    # aitchison norm percentiles gives the global scaling factor. This should
    # be done after truncation though.

    # Put back processed composition
    bary[mask] = temp
    return bary.reshape(dims)
