# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


# Package meta-data.
NAME = "EthSential"
DESCRIPTION = "Security analysis for Ethereum smart contracts"
# URL = "https://github.com/ConsenSys/mythril"
AUTHOR = "Daniel Dias"
AUTHOR_MAIL = None
REQUIRES_PYTHON = ">=3.6.0"

# If version is set to None then it will be fetched from __version__.py
VERSION = None

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


setup(
    name='ethsential',
    version=about["__version__"][1:],
    description='EthSential package for Python-Guide.org',
    long_description=readme,
    author='Daniel Dias',
    install_requires=[
        'docker==0.23.3',
        'pygls==0.9.0'
    ],
    # url='https://github.com/kennethreitz/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
