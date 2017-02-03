"""Multi scale retinex."""

from __future__ import division
import time
import numpy as np
from scipy.ndimage import gaussian_filter
np.seterr(divide='ignore', invalid='ignore')


def MultiScaleRetinex_3D(image, scales=[1, 10, 30]):
    """Multi scale retinex for 3 dimensional images.

    Parameters
    ----------
    image : 3d numpy array
        Input image/data/volume.

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
    start = time.time()
    print('applying multi-scale retinex filter...')

    scales = np.array(scales)  # sigma values
    msr = np.zeros(image.shape + (scales.size,))
    for i, sigma in enumerate(scales):
        print '.'
        msr[:, :, :, i] = np.log(image + 1) \
            - np.log(gaussian_filter(image, sigma, mode="constant", cval=0.0)
                     + 1)
    # remove nans
    msr = np.nan_to_num(msr)
    # weighted sum
    msr = np.sum(msr, 3) / scales.size
    msr = np.nan_to_num(msr)
    # return from logarithmic space
    msr = np.exp(msr-1)

    end = time.time()
    print 'Multi-scale retinex computed in:', (end - start), 'seconds'

    return msr
