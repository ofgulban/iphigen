"""Example script for multi-scale retinex on a single MR image."""

import os
import numpy as np
from nibabel import load, save, Nifti1Image

from retinex_for_mri.utils import truncate_and_scale
from retinex_for_mri.core import multi_scale_retinex_3d

# Load nifti
nii = load('/home/faruk/gdrive/Segmentator/brainbox32/010_northern_plains_gray_langur/LangurIndienPith_8390.nii.gz')
basename_vol1 = nii.get_filename().split(os.extsep, 1)[0]

# Preprocess
data = nii.get_data()
data = truncate_and_scale(data, percMin=0, percMax=100, zeroTo=1.0)

# Retinex
new_data = multi_scale_retinex_3d(data, scales=[1, 3, 10])

# Scale the data
new_data = truncate_and_scale(new_data, percMin=0, percMax=100, zeroTo=200)

# Save corrected image
out = Nifti1Image(np.squeeze(new_data), affine=nii.affine)
save(out, basename_vol1 + '_msr.nii.gz')
print('Finished.')
