[![DOI](https://zenodo.org/badge/76043117.svg)](https://zenodo.org/badge/latestdoi/76043117)
[![PyPI version](https://badge.fury.io/py/retinex_for_mri.svg)](https://badge.fury.io/py/retinex_for_mri)


## PyRetinex (work in progress)

Provides a simple commandline interface for applying _multi-scale retinex_ image enhancement. It supports 3D images too, such as magnetic resonance (MR) images.

## Dependencies

**[Python 3.6](https://www.python.org/downloads/release/python-363/)** or **[Python 2.7](https://www.python.org/download/releases/2.7/)** (compatible with both) and the following packages:

| Package                              | Tested version |
|--------------------------------------|----------------|
| [NumPy](http://www.numpy.org/)       | 1.14.2         |
| [SciPy](https://www.scipy.org/)      | 1.0.0          |
| [NiBabel](http://nipy.org/nibabel/)  | 2.2.0          |

## Installation

Clone this repository or download the latest release. In your commandline, change directory to folder of this package and run the following on your command line:
```
python setup.py install
```

# Usage
Simply apply retinex to an image with:
```
pyretinex /path/to/image.png
```
TODO: Put before after image here.

Selecting different scales gives different results:
```
pyretinex /path/to/image.png --scales 5 20 100
```
TODO: Put before after image here.

You can use this with nifti images too, simply call:
```
pyretinex_nifti /path/to/data.nii.gz
```
TODO: Put before after image here.

For other options, see:
```
pyretinex -h
```

## Support

Please use [github issues](https://github.com/ofgulban/retinex_for_mri/issues) to report bugs or make suggestions.

## License

The project is licensed under [GNU General Public License Version 3](http://www.gnu.org/licenses/gpl.html).

## References

This application is based on the following work:

* Jobson, D. J., Rahman, Z. U., & Woodell, G. A. (1997). A multiscale retinex for bridging the gap between color images and the human observation of scenes. IEEE Transactions on Image Processing, 6(7), 965–976. <http://doi.org/10.1109/83.597272>

* Petro, A. B., Sbert, C., & Morel, J. (2014). Multiscale Retinex. Image Processing On Line, 4, 71–88. <http://doi.org/10.5201/ipol.2014.107>
