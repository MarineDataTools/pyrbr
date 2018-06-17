from setuptools import setup
import os

ROOT_DIR='pyrbr'
with open(os.path.join(ROOT_DIR, 'VERSION')) as version_file:
    version = version_file.read().strip()

setup(name='pyrbr',
      version=version,
      description='Tool to parse RBR textfiles',
      url='https://github.com/MarineDataTools/pyrbr',
      author='Peter Holtermann',
      author_email='peter.holtermann@io-warnemuende.de',
      license='GPLv03',
      packages=['pyrbr'],
      scripts = [],
      entry_points={},
      package_data = {'':['VERSION']},
      zip_safe=False)


# TODO Depends on gsw, pyproj, pytz
