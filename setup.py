"""Iphigen setup.

To install, using the commandline do:
    pip install -e /path/to/iphigen

Notes for PyPI:
python setup.py sdist upload -r pypitest
python setup.py sdist upload -r pypi
"""


from setuptools import setup

VERSION = '1.0.0'

setup(name='iphigen',
      version=VERSION,
      description='Retinex & color balance algorithms for image enhancement.',
      url='https://github.com/ofgulban/iphigen',
      download_url=('https://github.com/ofgulban/iphigen/archive/'
                    + VERSION + '.tar.gz'),
      author='Omer Faruk Gulban',
      author_email='faruk.gulban@maastrichtuniversity.nl',
      license='BSD-3-Clause',
      packages=['iphigen'],
      install_requires=['numpy', 'scipy'],
      keywords=['mri', 'retinex', 'color', 'color balance'],
      entry_points={'console_scripts': [
          'iphigen = iphigen.iphigen_2d:main',
          'iphigen_nifti = iphigen.iphigen_nifti:main']},
      zip_safe=True)
