import os
from scipy.ndimage import generic_filter
import numpy as np
from nibabel import load, save, Nifti1Image


vol1 = load('/media/Data_Drive/RGB_to_HSL/Valentin/S1/T1_g_g_MSRCP.nii.gz')

basename = vol1.get_filename().split(os.extsep, 1)[0]
dirname = os.path.dirname(vol1.get_filename())
data = vol1.get_data()


def image_snr(input):
    """Calculate image SNR."""
    return np.mean(input)/np.std(input)


out = generic_filter(data, image_snr, size=10)

marian = Nifti1Image(out,
                     header=vol1.get_header(), affine=vol1.get_affine())
save(marian, os.path.join(dirname, '_SNR.nii.gz'))
