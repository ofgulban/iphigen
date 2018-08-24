"""Collection of simple, handy functions."""

import os
import numpy as np


def truncate_and_scale(data, pmin=2.5, pmax=97.5, zero_to=255):
    """Truncate and scale the data as a preprocessing step.

    Parameters
    ----------
    data : nd numpy array
        Data/image to be truncated and scaled.
    pmin : float, positive
        Minimum percentile to be truncated.
    pmax : float, positive
        Maximum percentile to be truncated.
    zero_to : float
        Data will be returned in the range from 0 to this number.

    Returns
    -------
    data : nd numpy array
        Truncated and scaled data/image.

    """
    # adjust minimum
    pmin, pmax = np.nanpercentile(data, [pmin, pmax])
    data[np.where(data < pmin)] = pmin
    data[np.where(data > pmax)] = pmax
    data = data - np.nanmin(data)
    # adjust maximum
    data = (1. / np.nanmax(data)) * data
    return data * zero_to


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
