#!/usr/bin/env python
from distutils.core import setup

setup(
    name='PurePyECC',
    version='0.1.0',
    author='Aljosha Judmayer',
    author_email='aljosha.j@3-volution.net',
    packages=['purepyecc', 'purepyecc.test'],
    scripts=['bin/alice.py','bin/bob.py'],
    url='http://TODO',
    license='LICENSE.txt',
    description='Pure python ECC arithmetic over binary curves.',
    long_description=open('README.txt').read(),
    install_requires=[
        "pycrypto  >= 2.6",
    ],
)
