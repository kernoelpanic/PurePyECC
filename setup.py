#!/usr/bin/env python
from distutils.core import setup

# install:
# $ python setup.py install --record /tmp/files.txt
# uninstall:
# $ cat /tmp/files.txt | xargs rm -rf

setup(
    name='PurePyECC',
    version='0.1.1',
    author='Aljosha Judmayer',
    author_email='kernoelpanic@3-volution.net',
    packages=['purepyecc', 'purepyecc.test'],
    url='https://github.com/kernoelpanic/PurePyECC',
    license='LICENSE.txt',
    description='PurePyECC should help you to learn the basics of ECC arithmetic over binary curves.',
    long_description=open('README.txt').read(),
)
