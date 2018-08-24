"""Default input parameters."""

filename = None
out_dir = None

retinex = False
intensity_balance = False
simplest_color_balance = False
simplex_color_balance = False

# retinex defaults
scales = [15, 80, 250]
scales_nifti = [1, 3, 10]

# intensity balance defaults
int_bal_perc = [1., 99.]  # intensity balance percentiles

# simplest color balance defaults
simplest_perc = [1., 99.]  # percentiles

# simplex color balance defaults
simplex_center = True
simplex_standardize = False
