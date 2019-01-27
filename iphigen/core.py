"""Core functions of Iphigen package."""

from __future__ import division
import time
import numpy as np
import compoda.core as coda
from scipy.ndimage import gaussian_filter
from iphigen.utils import truncate_range, set_range
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
    verbose: bool
        Print intermediate information. Useful to track progress when
        processing large images.

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
    # print('old:{} {}'.format(opmin, opmax))
    # print('new:{} {}'.format(npmin, npmax))
    scale_factor = opmax - opmin / (npmax - npmin)
    new_image *= scale_factor
    return new_image


def simplest_color_balance(image, pmin=1., pmax=99.):
    """Simplest color balance.

    Parameters
    ----------
    image: ndim numpy array
        Last dimension should contain channels (eg. RGB)
    pmin: float
        Percent minimum.
    pmax: float
        Percent maximum.

    Reference
    ---------
    Limare, N., Lisani, J., Morel, J., Petro, A. B., & Sbert, C. (2011).
    Simplest Color Balance. Image Processing On Line, 1(1), 125-133.
    http://doi.org/10.5201/ipol.2011.llmps-scb

    """
    dims = image.shape
    for d in range(dims[-1]):
        image[..., d] = truncate_range(image[..., d], pmin=pmin, pmax=pmax)
        image[..., d] = set_range(image[..., d], zero_to=255)
    return image


def simplex_color_balance(bary, center=True, standardize=False,
                          trunc_max=False):
    """Compositional data based method for color balance.

    Highly experimental!

    Parameters
    ----------
    bary: numpy.ndarray
        Barycentric coordinates. Sum of all channels should add up to 1
        (closed).
    center: bool
        Center barycentric coordinates (similar to de-meaning). Single-hue
        dominated images will be balanced to cover all hues.
    standardize: bool
        Standardize barycentric coordinates. Standardized compositions make
        better use of the simplex space dynamic range.
    trunc_max: bool
        Truncate maximum barycentric coordinates to eliminate extreme hues that
        are not prevalent in the image.

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
