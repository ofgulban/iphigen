"""Multi scale retinex."""

from __future__ import division
import time
import numpy as np
from scipy.ndimage import gaussian_filter
np.seterr(divide='ignore', invalid='ignore')


def MultiScaleRetinex_3D(image, scales=[1, 10, 30]):
    """Multi scale retinex function for mri data."""
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
