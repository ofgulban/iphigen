"""Collection of simple, handy functions."""

import numpy as np


def truncate_range(data, percMin=0.25, percMax=99.75, discard_zeros=True):
    """Truncate too low and too high values.

    Parameters
    ----------
    data : np.ndarray
        Image to be truncated.
    percMin : float
        Percentile minimum.
    percMax : float
        Percentile maximum.
    discard_zeros : bool
        Discard voxels with value 0 from truncation.

    Returns
    -------
    data : np.ndarray
        Truncated data.
    pMin : float
        Minimum truncation threshold which is used.
    pMax : float
        Maximum truncation threshold which is used.

    """
    if discard_zeros:
        msk = ~np.isclose(data, 0.)
        pMin, pMax = np.nanpercentile(data[msk], [percMin, percMax])
    else:
        pMin, pMax = np.nanpercentile(data, [percMin, percMax])
    temp = data[~np.isnan(data)]
    temp[temp < pMin], temp[temp > pMax] = pMin, pMax  # truncate min and max
    data[~np.isnan(data)] = temp
    if discard_zeros:
        data[~msk] = 0  # put back masked out voxels
    return data, pMin, pMax


def scale_range(data, scale_factor=500, delta=0, discard_zeros=True):
    """Scale values as a preprocessing step.

    Parameters
    ----------
    data : np.ndarray
        Image to be scaled.
    scale_factor : float
        Lower scaleFactors provides faster interface due to loweing the
        resolution of 2D histogram ( 500 seems fast enough).
    delta : float
        Delta ensures that the max data points fall inside the last bin
        when this function is used with histograms.
    discard_zeros : bool
        Discard voxels with value 0 from truncation.

    Returns
    -------
    data: np.ndarray
        Scaled image.

    """
    if discard_zeros:
        msk = ~np.isclose(data, 0)
    else:
        msk = np.ones(data.shape, dtype=bool)
    scale_factor = scale_factor - delta
    data[msk] = data[msk] - np.nanmin(data[msk])
    data[msk] = scale_factor / np.nanmax(data[msk]) * data[msk]
    if discard_zeros:
        data[~msk] = 0  # put back masked out voxels
    return data
