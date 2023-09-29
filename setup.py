from setuptools import find_packages
from setuptools import setup

setup(
    name='led',
    version='0.0.1',
    packages=find_packages('app'),
    package_dir={'': 'app'},
    author='Tommy Kardach',
    author_email='tommy@kardach.com',
)