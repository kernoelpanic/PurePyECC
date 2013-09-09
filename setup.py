#!/usr/bin/env python
from distutils.core import setup

setup(
    name='PurePyECC',
    version='0.1.0',
    author='Aljosha Judmayer',
    author_email='dev@3-volution.net',
    packages=['purepyecc', 'purepyecc.test'],
    scripts=['bin/alice.py','bin/bob.py'],
    url='https://github.com/kernoelpanic/PurePyECC',
    license='LICENSE.txt',
    description='Pure python ECC arithmetic over binary curves.',
    long_description=open('README.txt').read(),
    install_requires=["pycrypto  >= 2.6"],
)
