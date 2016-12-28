"""Aniso tests (WIP)."""

import os
from nibabel import load, save, Nifti1Image
from aniso import anisodiff3

"""Load Data"""
#
nii = load('/home/faruk/Data/Faruk/T2s.nii.gz')

basename_vol1 = nii.get_filename().split(os.extsep, 1)[0]
dirname = os.path.dirname(nii.get_filename())
niiHeader, niiAffine = nii.header, nii.affine

data = nii.get_data()

test = anisodiff3(data, niter=2, kappa=100, gamma=0.1, option=1)
# test = anisodiff3(data, niter=2, kappa=70, gamma=0.2, option=1)
# test = anisodiff3(data*255, niter=1, kappa=50, gamma=0.1, option=1)

out = Nifti1Image(test, header=niiHeader, affine=niiAffine)
save(out, basename_vol1 + '_ANISO.nii.gz')
print "Done."
