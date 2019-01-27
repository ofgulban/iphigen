"""Collection of simple, handy functions."""

import os
import numpy as np


def truncate_range(data, pmin=0.25, pmax=99.75, discard_zeros=True):
    """Truncate too low and too high values.

    Parameters
    ----------
    data : np.ndarray
        Image to be truncated.
    pmin : float
        Percentile minimum.
    pmax : float
        Percentile maximum.
    discard_zeros : bool
        Discard voxels with value 0 from truncation.

    Returns
    -------
    data : np.ndarray

    """
    if discard_zeros:
        msk = ~np.isclose(data, 0)
        thr_min, thr_max = np.nanpercentile(data[msk], [pmin, pmax])
    else:
        thr_min, thr_max = np.nanpercentile(data, [pmin, pmax])
    temp = data[~np.isnan(data)]
    # truncate min and max
    temp[temp < thr_min], temp[temp > thr_max] = thr_min, thr_max
    data[~np.isnan(data)] = temp
    if discard_zeros:
        data[~msk] = 0  # put back masked out voxels
    return data


def set_range(data, zero_to=255, discard_zeros=True):
    """Scale values as a preprocessing step.

    Parameters
    ----------
    data : np.ndarray
        Image to be scaled.
    zero_to : float
        TODO
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
    data[msk] -= np.nanmin(data[msk])
    data[msk] *= (zero_to / np.nanmax(data[msk]))
    if discard_zeros:
        data[~msk] = 0  # put back masked out elements
    return data


def parse_filepath(filepath):
    """Load images with different extensions.

    Parameters
    ----------
    filepath: string
        Input name that will be parsed into path, basename and extension

    Returns
    -------
    data: ndim numpy array
        Image data.
    dirname: string
        File directory.
    basename: string
        File name without directory and extension.
    ext: string
        File extension.

    """
    path = os.path.normpath(filepath)
    dirname = os.path.dirname(path)
    filename = path.split(os.sep)[-1]
    basename, ext = filename.split(os.extsep, 1)
    return dirname, basename, ext


def prepare_scale_suffix(scales):
    """Prepare scale identifier suffix.

    Parameters
    ----------
    scales: list

    Returns
    -------
    id: string

    """
    id = ''
    for s in scales:
        id += '_{}'.format(s)
    return id
