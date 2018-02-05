from setuptools import setup, find_packages
import os
HERE = os.path.dirname(__file__)
def read(fname):
    return open(os.path.join(HERE, fname)).read()

# creates version_string
exec(open(os.path.join(HERE, "perseuspy", "version.py")).read())

setup(name='perseuspy',
        version=version_string, # read from version.py
        description='Utilities for integrating python scripts into Perseus workflows',
        long_description=read('README.rst'),
        url='http://www.github.com/jdrudolph/perseuspy',
        author='Jan Rudolph',
        author_email='jan.daniel.rudolph@gmail.com',
        license='MIT',
        packages=find_packages(),
        install_requires=['pandas >= 0.21', 'networkx >= 2.1'],
        test_suite = 'nose.collector',
        tests_require= ['nose']
) 
