#!/usr/bin/env python2
# Copyright 2018-present, Tencent.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from setuptools import setup, find_packages
import sys

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    reqs = f.read()

setup(
    name='drqa',
    version='0.1.0',
    description='Chinese spelling check',
    long_description=readme,
    license=license,
    python_requires='>=2.7',
    include_package_data=True,
    exclude_package_date={'': ['.gitignore']},
    packages=find_packages(exclude=('data')),
    install_requires=reqs.strip().split('\n'),
    dependency_links=[
       'https://github.com/kpu/kenlm/archive/master.zip'
    ]
)