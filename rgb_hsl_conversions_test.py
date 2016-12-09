"""Pseudo-color test for mri data."""

from __future__ import division
import os
import numpy as np
from nibabel import load, save, Nifti1Image
from AutoScale import AutoScale
from rgb2hsl import rgb2hsl, hsl2rgb
np.seterr(divide='ignore', invalid='ignore')

"""Load Data"""
#
vol1 = load('/media/Data_Drive/test4/S05_SES1_T1_divT2s_pt5_DIF.nii')
vol2 = load('/media/Data_Drive/test4/S05_SES1_T1_divPD_pt5_DIF.nii')
vol3 = load('/media/Data_Drive/test4/S05_SES1_PD_divT2s_pt5_DIF.nii')

basename = vol1.get_filename().split(os.extsep, 1)[0]
dirname = os.path.dirname(vol1.get_filename())
niiHeader, niiAffine = vol1.get_header(), vol1.get_affine()
shape = vol1.shape + (3,)

# Preprocess
vol1 = AutoScale(vol1.get_data(), percMin=0.1, percMax=99.0, zeroTo=1.0)
vol2 = AutoScale(vol2.get_data(), percMin=0.1, percMax=99.0, zeroTo=1.0)
vol3 = AutoScale(vol3.get_data(), percMin=0.1, percMax=99.0, zeroTo=1.0)

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

print "Done."

# -----------------------------------------------------------------------------
# TESTS
"""Can be converted to test scripts, Do not delete"""

# flat = np.zeros([5, 3])
# flat[0, :] = [1, 0.22, 0]
# flat[1, :] = [0, 1, 0.33]
# flat[2, :] = [0.666, 0.12, 1]
# flat[3, :] = [1, 1, 1]
#
# flat.shape
#
# hsl = rgb2hsl(flat)
# hsl
#
# rgb = hsl2rgb(hsl)
# rgb

# -----------------------------------------------------------------------------
