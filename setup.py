# -*- coding: utf-8 -*-
import os
import sys

try:
    from setuptools import setup
    # hush pyflakes
    setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='requests-aws',
    version='0.1.5',
    author='Paul Tax',
    author_email='paultax@gmail.com',
    include_package_data=True,
    install_requires = ['requests>=0.14.0'],
    py_modules=['awsauth'],
    url='https://github.com/tax/python-requests-aws',
    license='BSD licence, see LICENCE.txt',
    description='AWS authentication for Amazon S3 for the python requests module',
    long_description=open('README.md').read(),
)

