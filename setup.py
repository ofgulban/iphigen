"""retinex_for_mri setup.

To install, using the commandline do:
    pip install -e /path/to/retinex_for_mri

"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='retinex_for_mri',
      version='0.2.6',
      description='Retinex algorithm for MRI data.',
      url='https://github.com/ofgulban/retinex_for_mri',
      download_url='https://github.com/ofgulban/retinex_for_mri/releases/tag/0.2.6',
      author='Omer Faruk Gulban',
      author_email='',
      license='GNU Geneal Public License Version 3',
      packages=['retinex_for_mri'],
      install_requires=['numpy', 'scipy'],
      zip_safe=False)
