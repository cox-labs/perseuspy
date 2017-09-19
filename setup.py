from setuptools import setup, find_packages

from perseuspy import __version__

import os
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='perseuspy',
        version=__version__,
        description='Utilities for integrating python scripts into Perseus workflows',
        long_description=read('README.rst'),
        url='http://www.github.com/jdrudolph/perseuspy',
        author='Jan Rudolph',
        author_email='jan.daniel.rudolph@gmail.com',
        license='MIT',
        packages=find_packages(),
        install_requires=['pandas >= 0.19', 'networkx'],
        test_suite = 'nose.collector',
        test_require= ['nose']
) 

