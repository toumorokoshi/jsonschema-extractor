#!/usr/bin/env python
import glob
import os
import sys
from setuptools import setup, find_packages

is_release = False
if "--release" in sys.argv:
    is_release = True
    sys.argv.remove("--release")

base = os.path.dirname(os.path.abspath(__file__))

README_PATH = os.path.join(base, "README.rst")

install_requires = [
    'attrs',
    'schematics>=2.0.0',
    'six',
    'jinja2',
    'swagger-schema>=0.4.0',
    'pyyaml',
]

tests_require = []

setup(name='attrs-jsonschema',
      setup_requires=["vcver"],
      vcver={
          "is_release": is_release,
          "path": base
      },
      description=(
          "convert a attrs annotation to json a json schema."
      ),
      long_description=open(README_PATH).read(),
      author='Yusuke Tsutsumi',
      author_email='yusuke@tsutsumi.io',
      url='https://github.com/toumorokoshi/attrs-jsonschema',
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      tests_require=tests_require
)
