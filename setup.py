"""pyretinex setup.

To install, using the commandline do:
    pip install -e /path/to/pyretinex

Notes for PyPI:
python setup.py sdist upload -r pypitest
python setup.py sdist upload -r pypi
"""


from setuptools import setup

VERSION = '1.0.0'

setup(name='pyretinex',
      version=VERSION,
      description='Retinex algorithm implemented for MRI data.',
      url='https://github.com/ofgulban/retinex_for_mri',
      download_url=('https://github.com/ofgulban/retinex_for_mri/archive/'
                    + VERSION + '.tar.gz'),
      author='Omer Faruk Gulban',
      author_email='faruk.gulban@maastrichtuniversity.nl',
      license='GNU General Public License Version 3',
      packages=['pyretinex'],
      install_requires=['numpy', 'scipy'],
      keywords=['mri', 'retinex'],
      entry_points={'console_scripts': [
          'pyretinex = pyretinex.__main__:main']},
      zip_safe=True)
