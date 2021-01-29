#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

base = os.path.dirname(os.path.abspath(__file__))

README_PATH = os.path.join(base, "README.rst")

install_requires = []

if sys.version_info < (3, 4):
    install_requires.append("enum34")

if sys.version_info < (3, 5):
    install_requires.append("typing")

tests_require = []

setup(
    name="jsonschema-extractor",
    use_scm_version={
        "relative_to": __file__,
    },
    setup_requires=["setuptools_scm"],
    description=("a framework to extract jsonschema's from a variety of models."),
    long_description=open(README_PATH).read(),
    author="Yusuke Tsutsumi",
    author_email="yusuke@tsutsumi.io",
    url="https://github.com/toumorokoshi/attrs-jsonschema",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Software Distribution",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    tests_require=tests_require,
)
