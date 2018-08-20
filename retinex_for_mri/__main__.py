"""Retinex for magnetic resonance images."""

import os
import argparse
import numpy as np
from nibabel import load, save, Nifti1Image
from retinex_for_mri.core import multi_scale_retinex_3d
from retinex_for_mri import __version__
import retinex_for_mri.config as cfg


def main():
    """Command line call argument parsing."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'filename',  metavar='path',
        help="Path to nii file with image data."
        )
    parser.add_argument(
        '--scales', nargs='+', type=int, required=False,
        metavar=' '.join(str(e) for e in cfg.scales),
        help="Retinex scales."
        )

    args = parser.parse_args()

    cfg.scales = args.scales

    # Welcome message
    welcome_str = 'Retinex for MRI {}'.format(__version__)
    welcome_decor = '=' * len(welcome_str)
    print('{}\n{}\n{}'.format(welcome_decor, welcome_str, welcome_decor))

    # Load nifti
    nii = load(args.filename)
    basename = nii.get_filename().split(os.extsep, 1)[0]
    data = nii.get_data()

    print('Selected scales: {}'.format(cfg.scales))

    # Multi-scale retinex
    new_data = multi_scale_retinex_3d(data, scales=cfg.scales)

    # Scale new data approximately to original dynamic range
    opmin, opmax = np.nanpercentile(data, [2.5, 97.5])
    npmin, npmax = np.nanpercentile(new_data, [2.5, 97.5])
    odist = opmax - opmin
    ndist = npmax - npmin
    scale_factor = odist / ndist
    new_data *= scale_factor

    # Save corrected image
    print('Saving...')
    id_alg = 'MSR'  # algorithm identifier
    id_scl = ''  # scale identifier
    for s in cfg.scales:
        id_scl += '_{}'.format(s)
    out_name = '{}_{}{}.nii.gz'.format(basename, id_alg, id_scl)
    out = Nifti1Image(np.squeeze(new_data), affine=nii.affine)
    save(out, out_name)
    print('Finished.')


if __name__ == "__main__":
    main()
