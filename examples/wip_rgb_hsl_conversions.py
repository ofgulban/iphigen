"""Example script for converting 3 channel RGB-like MRI data to HSL."""

from __future__ import division
import os
import numpy as np
from nibabel import load, save, Nifti1Image
from retinex_for_mri.conversions import rgb2hsl, hsl2rgb
from retinex_for_mri.utils import truncate_and_scale
np.seterr(divide='ignore', invalid='ignore')

"""Load Data"""
#
vol1 = load('/path/to/file1.nii')
vol2 = load('/path/to/file2.nii')
vol3 = load('/path/to/file3.nii')

basename = vol1.get_filename().split(os.extsep, 1)[0]
dirname = os.path.dirname(vol1.get_filename())
niiHeader, niiAffine = vol1.get_header(), vol1.get_affine()
shape = vol1.shape + (3,)

# Preprocess
vol1 = truncate_and_scale(vol1.get_data(), percMin=0.1, percMax=99.0)
vol2 = truncate_and_scale(vol2.get_data(), percMin=0.1, percMax=99.0)
vol3 = truncate_and_scale(vol3.get_data(), percMin=0.1, percMax=99.0)

rgb = np.zeros(shape)
rgb[:, :, :, 0] = vol1
del vol1
rgb[:, :, :, 1] = vol2
del vol2
rgb[:, :, :, 2] = vol3
del vol3

# RGB to HSL
flat = rgb.reshape(shape[0]*shape[1]*shape[2], shape[3])
hsl = rgb2hsl(flat)
hsl = hsl.reshape(shape)

out = Nifti1Image(np.squeeze(hsl[:, :, :, 0]),
                  header=niiHeader, affine=niiAffine)
save(out, os.path.join(dirname, 'TEST_hue.nii.gz'))
out = Nifti1Image(np.squeeze(hsl[:, :, :, 1]),
                  header=niiHeader, affine=niiAffine)
save(out, os.path.join(dirname, 'TEST_sat.nii.gz'))
out = Nifti1Image(np.squeeze(hsl[:, :, :, 2]),
                  header=niiHeader, affine=niiAffine)
save(out, os.path.join(dirname, 'TEST_lum.nii.gz'))

# HSL to RGB
flat = hsl.reshape(shape[0]*shape[1]*shape[2], shape[3])
rgb = hsl2rgb(flat)
rgb = rgb.reshape(shape)

out = Nifti1Image(np.squeeze(rgb[:, :, :, 0]),
                  header=niiHeader, affine=niiAffine)
save(out, os.path.join(dirname, 'TEST_red.nii.gz'))
out = Nifti1Image(np.squeeze(rgb[:, :, :, 1]),
                  header=niiHeader, affine=niiAffine)
save(out, os.path.join(dirname, 'TEST_green.nii.gz'))
out = Nifti1Image(np.squeeze(rgb[:, :, :, 2]),
                  header=niiHeader, affine=niiAffine)
save(out, os.path.join(dirname, 'TEST_blue.nii.gz'))

print("Done.")
