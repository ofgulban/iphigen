[![DOI](https://zenodo.org/badge/76043117.svg)](https://zenodo.org/badge/latestdoi/76043117)
[![PyPI version](https://badge.fury.io/py/retinex_for_mri.svg)](https://badge.fury.io/py/retinex_for_mri)


## Retinex for MRI (work in progress)

Currently this package is not intended for general use. However if you do use it and find it useful, please cite it with the Zenodo DOI:
* [https://doi.org/10.5281/zenodo.592341](https://doi.org/10.5281/zenodo.592341)

## Dependencies

**[Python 2.7](https://www.python.org/download/releases/2.7/)** or **[Python 3.6](https://www.python.org/downloads/release/python-363/)** (compatible with both) and the following packages:

| Package                              | Tested version |
|--------------------------------------|----------------|
| [NumPy](http://www.numpy.org/)       | 1.14.2         |
| [SciPy](https://www.scipy.org/)      | 1.0.0          |
| [NiBabel](http://nipy.org/nibabel/)  | 2.2.0          |

## Installation & Usage

To install, simply clone the repository or download the latest release and run the following on your command line:
```
pip install -e /path/to/retinex_for_mri
```

**NOTE:** This repository is still in development and example scripts prefixed with **wip** are not yet prepared for general usage.
*However*, if you would like to use the core functions please see the [dosctrings](https://en.wikipedia.org/wiki/Docstring) of [**core.py**](retinex_for_mri/core.py).

## Support

Please use [github issues](https://github.com/ofgulban/retinex_for_mri/issues) to report bugs or make suggestions.

## License

The project is licensed under [GNU General Public License Version 3](http://www.gnu.org/licenses/gpl.html).

## References
This application is based on the following work:

* Jobson, D. J., Rahman, Z. U., & Woodell, G. A. (1997). A multiscale retinex for bridging the gap between color images and the human observation of scenes. IEEE Transactions on Image Processing, 6(7), 965–976. http://doi.org/10.1109/83.597272

* Petro, A. B., Sbert, C., & Morel, J. (2014). Multiscale Retinex. Image Processing On Line, 4, 71–88. http://doi.org/10.5201/ipol.2014.107
