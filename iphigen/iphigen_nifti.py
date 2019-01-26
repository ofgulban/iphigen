"""MRI data processing with retinex and balance methods."""

from __future__ import division
import os
import numpy as np
import nibabel as nb
from iphigen import core, utils
from iphigen.ui import user_interface, display_welcome_message
import iphigen.config as cfg


def main():
    """Iphigen processes for nifti images."""
    user_interface()
    display_welcome_message()

    # Load data
    data, affine, dirname, basename, ext = [], [], [], [], []
    nr_fileinputs = len(cfg.filename)
    print('Selected file(s):')
    for i in range(nr_fileinputs):
        nii = nb.load(cfg.filename[i])
        affine.append(nii.affine)
        parses = utils.parse_filepath(cfg.filename[i])
        data.append(np.squeeze(nii.get_data()))
        print('  Name: {}'.format(cfg.filename[i]))
        print('  Dimensions: {}'.format(data[i].shape))
        if cfg.out_dir:
            dirname.append(cfg.out_dir)
        else:
            dirname.append(parses[0])
        basename.append(parses[1])
        ext.append(parses[2])

    # Reorganize data
    data = np.asarray(data)
    data = data.transpose([1, 2, 3, 0])
    # Compute intensity
    inten = np.sum(data, axis=-1)
    # Compute barycentic coordinates (equivalent to intensity for 0-simplex)
    bary = data / inten[..., None]

    suf = ''  # suffix
    # TODO: consider zero_to option for MRI data
    if cfg.intensity_balance:
        raise ValueError('Intensity balance not implemented.')
        # print('Applying intensity balance...')
        # print('  Percentiles: {}'.format(cfg.int_bal_perc))
        # suf = suf + '_IB'
        # inten = utils.truncate_and_scale(
        #     inten, pmin=cfg.int_bal_perc[0], pmax=cfg.int_bal_perc[1],
        #     zero_to=255*data.shape[-1])
        # data = bary * inten[..., None]
        # # Update barycentic coordinates
        # bary = data / inten[..., None]

    if cfg.retinex:
        print('Applying multi-scale retinex with barycenter preservation (MSRBP)...')
        print('  Selected scales: {}'.format(cfg.scales_nifti))
        suf = suf + '_MSRBP' + utils.prepare_scale_suffix(cfg.scales_nifti)
        new_inten = core.multi_scale_retinex(inten, scales=cfg.scales_nifti)
        # Scale back to the approximage original intensity range
        inten = core.scale_approx(new_inten, inten)

    if cfg.simplex_color_balance:
        print('Applying simplex color balance...')
        print('  Centering: {}'.format(cfg.simplex_center))
        print('  Standardize: {}'.format(cfg.simplex_standardize))
        suf = suf + '_SimplexCB'
        bary = core.simplex_color_balance(bary)

    # Insert back the processed intensity image
    data = bary * inten[..., None]

    if cfg.simplest_color_balance:
        print('Applying simplest color balance...')
        print('  Percentiles: {}'.format(cfg.int_bal_perc))
        suf = suf + '_SimplestCB'
        data = core.simplest_color_balance(
            data, pmin=cfg.simplest_perc[0], pmax=cfg.simplest_perc[1])

    # Check at least one operation is selected before saving anything
    if sum([cfg.retinex, cfg.intensity_balance, cfg.simplex_color_balance,
            cfg.simplest_color_balance]) > 0:
        print('Saving output(s)...')
        for i in range(nr_fileinputs):
            # Generate output path
            out_basepath = os.path.join(dirname[i],
                                        '{}{}'.format(basename[i], suf))
            out_path = out_basepath + os.extsep + ext[i]
            # Create nifti image and save
            img = nb.Nifti1Image(data[..., i], affine=affine[i])
            nb.save(img, out_path)
            print('  {} is saved.\n'.format(out_path))
    else:
        print('No operation selected, not saving anything.')
    print('Finished.')


if __name__ == "__main__":
    main()
