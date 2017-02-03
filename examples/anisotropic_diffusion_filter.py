"""Example script for 3D anisotropic diffusion filter."""

import os
from nibabel import load, save, Nifti1Image
from retinex_for_mri.filters import anisodiff3

# Load nifti
nii = load('/path/to/your/file.nii.gz')
basename_nii = nii.get_filename().split(os.extsep, 1)[0]
niiHeader, niiAffine = nii.header, nii.affine

data = nii.get_data()

data = anisodiff3(data, niter=2, kappa=100, gamma=0.1, option=1)

out = Nifti1Image(data, header=niiHeader, affine=niiAffine)
save(out, basename_nii + '_aniso.nii.gz')
print "Done."
