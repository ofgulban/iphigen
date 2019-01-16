"""Example script for multi-scale retinex on a single MR image."""

import os
import nibabel as nb

from iphigen.core import multi_scale_retinex, scale_approx

# Load nifti image
input_path = '/path/to/file.nii.gz'
nii = nb.load(input_path)
data = nii.get_data()

# Apply retinex
new_data = multi_scale_retinex(data, scales=[1, 3, 10])

# Scale the data to approximately the same range as before
new_data = scale_approx(new_data, data)

# Save corrected image
out = nb.Nifti1Image(new_data, affine=nii.affine)
basename = input_path.split(os.extsep, 1)[0]
nb.save(out, '{}_MSR.nii.gz'.format(basename))
print('Finished.')
