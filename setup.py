#!/usr/bin/env python
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='d3shims',
    version='0.1.1',

    description='Shim functions to generate D3 plots',
    long_description=long_description,

    url='https://github.com/nicktimko/d3shims',

    author='Nick Timkovich',
    author_email='npt@u.northwestern.edu',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='d3js networks graphs networkx jupyter ipython',

    # packages=['d3shims'],
    py_modules=["d3shims"],

    # install_requires=['networkx'],
)
