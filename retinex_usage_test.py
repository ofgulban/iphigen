""" Example script for multi-scale retinex."""

import os
import numpy as np
from nibabel import load, save, Nifti1Image
from conversions import AutoScale
from retinex import MultiScaleRetinex_3D

# Load data
nii = load('/path/to/your/file.nii.gz')
basename_vol1 = nii.get_filename().split(os.extsep, 1)[0]

# Preprocess
data = nii.get_data()
data = AutoScale(data, percMin=0, percMax=100, zeroTo=1.0)

# Retinex
new_data = MultiScaleRetinex_3D(data, scales=[1, 3, 10])

# Scale the data
new_data = AutoScale(new_data, percMin=0, percMax=100, zeroTo=200)

# Save corrected image
out = Nifti1Image(np.squeeze(new_data), affine=nii.affine)
save(out, basename_vol1 + '_msr.nii.gz')
print 'Finished.'
