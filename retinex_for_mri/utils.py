"""Collection of simple, handy functions."""

import numpy as np


def truncate_and_scale(data, percMin=0.01, percMax=99.9, zeroTo=1.0):
    """Truncate and scale the data as a preprocessing step.

    Parameters
    ----------
    data : nd numpy array
        Data/image to be truncated and scaled.
    percMin : float, positive
        Minimum percentile to be truncated.
    percMax : float, positive
        Maximum percentile to be truncated.
    zeroTo : float
        Data will be returned in the range from 0 to this number.

    Returns
    -------
    data : nd numpy array
        Truncated and scaled data/image.

    """
    # adjust minimum
    percDataMin = np.percentile(data, percMin)
    data[np.where(data < percDataMin)] = percDataMin
    data = data - data.min()

    # adjust maximum
    percDataMax = np.percentile(data, percMax)
    data[np.where(data > percDataMax)] = percDataMax
    data = 1./data.max() * data
    return data * zeroTo
