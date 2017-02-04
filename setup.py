"""retinex_for_mri setup.

To install, using the commandline do:
    pip install -e /path/to/retinex_for_mri

"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='retinex_for_mri',
      version='0.2.9',
      description='Retinex algorithm for MRI data.',
      url='https://github.com/ofgulban/retinex_for_mri',
      download_url='https://github.com/ofgulban/retinex_for_mri/archive/0.2.9.tar.gz',
      author='Omer Faruk Gulban',
      author_email='faruk.gulban@maastrichtuniversity.nl',
      license='GNU General Public License Version 3',
      packages=['retinex_for_mri'],
      install_requires=['numpy', 'scipy'],
      keywords=['mri'],
      zip_safe=True)
