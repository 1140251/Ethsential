# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


# Package meta-data.
NAME = "EthSential"
DESCRIPTION = "Security analysis for Ethereum smart contracts"
URL = "https://github.com/1140251/Ethsential"
AUTHOR = "Daniel Dias"
AUTHOR_MAIL = "1140251@isep.ipp.pt"
REQUIRES_PYTHON = ">=3.6.0"

# If version is set to None then it will be fetched from __version__.py
VERSION = None

with open('README.md', encoding="utf-8") as f:
    readme = '\n' + f.read()

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
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_mail=AUTHOR_MAIL,
    install_requires=[
        'docker==4.2.1',
        'pygls==0.9.0',
        'joblib==0.16.0',
        'solidity_parser==0.0.7'
    ],
    url='https://github.com/1140251/Ethsential',
    license="Apache-2.0",
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={"console_scripts": ["ethsent=ethsential.__main__:main"]},
)
