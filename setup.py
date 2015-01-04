import os
import sys
from setuptools import setup, find_packages

version = '0.1.1'

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


setup(name='android-localization-helper',
      version=version,
      description=('Android localization helper'),
      long_description='\n\n'.join((read('README.md'), read('CHANGELOG'))),
      classifiers=[
          'License :: OSI Approved :: BSD License',
          'Intended Audience :: Developers',
          'Programming Language :: Python'],
      keywords='android localization translation translate',
      author='Jordan Jozwiak',
      author_email='jordanjoz1@gmail.com',
      url='https://github.com/jordanjoz1/android-localization-helper',
      license='MIT',
      py_modules=['translation_helper'],
      namespace_packages=[],
      install_requires = [],
      entry_points={
          'console_scripts': [
              'android-localization-helper = translation_helper:main']
      },
      include_package_data = False)