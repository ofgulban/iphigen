"""retinex_for_mri setup.

To install, using the commandline do:
    pip install -e /path/to/retinex_for_mri

Notes for PyPI:
python setup.py sdist upload -r pypitest
python setup.py sdist upload -r pypi
"""


from setuptools import setup

VERSION = '0.3.0'

setup(name='retinex_for_mri',
      version=VERSION,
      description='Retinex algorithm for MRI data.',
      url='https://github.com/ofgulban/retinex_for_mri',
      download_url=('https://github.com/ofgulban/retinex_for_mri/archive/'
                    + VERSION + '.tar.gz'),
      author='Omer Faruk Gulban',
      author_email='faruk.gulban@maastrichtuniversity.nl',
      license='GNU General Public License Version 3',
      packages=['retinex_for_mri'],
      install_requires=['numpy', 'scipy'],
      keywords=['mri', 'retinex'],
      zip_safe=True)
