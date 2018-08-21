"""Collection of simple, handy functions."""

import os
import cv2
import numpy as np
import nibabel as nb


def truncate_and_scale(data, percMin=2.5, percMax=97.5, zeroTo=255):
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
    pmin, pmax = np.percentile(data, [percMin, percMax])
    data[np.where(data < pmin)] = pmin
    data[np.where(data > pmax)] = pmax
    data = data - data.min()

    # adjust maximum
    data = (1. / data.max()) * data
    return data * zeroTo


def load_data(filepath):
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

    # load data depending on extension
    ext = ext.lower()  # for capital extensions
    if ext in ['nii', 'nii.gz']:
        print('Loading nifti image...')
        nii = nb.load(filepath)
        data = nii.get_data()
    elif ext is 'npy':
        print('Loading numpy array...')
        data = np.load(filepath)
    elif ext in ['bmp', 'dib', 'jpeg', 'jpg', 'jpe', 'jp2', 'png', 'pbm',
                 'pgm', 'ppm', 'sr', 'ras', 'tiff', 'tif']:
        print('Loading RGB image...')
        data = cv2.imread(filepath)
    else:
        raise ValueError('Unrecognized file extension.')
    return data, dirname, basename, ext


def save_data(data, basepath, ext, original_filepath=None):
    """Save images depending op their original extensionsself.

    Parameters
    ----------
    data: ndim numpy array
        Image data.
    basepath: string
        File name without directory and extension.
    ext: string
        File extension.
    original_filepath: string
        Full path of the original input file. NOTE: I could not find a way to
        avoid having this when saving nifti files with original headers.

    """
    if ext in ['nii', 'nii.gz']:
        print('Saving nifti image...')
        affine = (nb.load(original_filepath)).affine
        out = nb.Nifti1Image(np.squeeze(data), affine=affine)
        out_path = basepath + os.extsep + ext
        nb.save(out, out_path)
    elif ext is 'npy':
        print('Saving numpy array...')

    elif ext in ['bmp', 'dib', 'jpeg', 'jpg', 'jpe', 'jp2', 'png', 'pbm',
                 'pgm', 'ppm', 'sr', 'ras', 'tiff', 'tif']:
        print('Saving RGB image...')
