perseuspy README
================

.. image:: https://readthedocs.org/projects/perseuspy/badge/?version=latest
    :target: http://perseuspy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. sphinx-inclusion-marker-do-not-remove

.. image:: https://travis-ci.org/jdrudolph/perseuspy.svg?branch=master
    :target: https://travis-ci.org/jdrudolph/perseuspy

Utility and covenience functions for Python-Perseus interop.
Building on the `pandas` package. If you intend to develop
a plugin for Perseus, please see `PluginInterop <https://www.github.com/jdrudolph/PluginInterop/>`_.

Installation
------------
Install using pip directly from `github`:

.. code:: bash

    pip install git+https://github.com/jdrudolph/perseuspy.git

Usage
------------
You can use `perseuspy` just like any other python module.


.. code:: python

    # import a monkey-patched version of pandas
    from perseuspy import pd
    df = pd.read_perseus('matrix1.txt')
    df2 = df.dropna()
    df2.to_perseus('matrix2.txt')


Plugin template
---------------
The following snippet can be used as a starting point
for python scripting in Perseus.

.. code:: python

    import sys
    from perseuspy import pd
    from perseuspy.parameters import *
    _, paramfile, infile, outfile = sys.argv # read arguments from the command line
    parameters = parse_parameters(paramfile) # parse the parameters file
    df = pd.read_perseus(infile) # read the input matrix into a pandas.DataFrame
    some_value = doubleParam(parameters, 'some value') # extract a parameter value
    df2 = some_value / df.drop('Name', 1)
    df2.to_perseus(outfile) # write pandas.DataFrame in Perseus txt format
    
Network Plugin template
---------------
The following snippet can be used as a starting point
for python scripting in Perseus (for networks).

.. code:: python

    import sys
    import networkx as nx
    from perseuspy import pd
    from perseuspy import readNetworks, writeNetworks
    allDicts = readNetworks(sys.argv[2]) # read networks from perseus created files
    newAllDicts = allDicts
    writeNetworks(sys.argv[3], newAllDicts) # write networks from newallDicts


Generating the documentation
----------------------------
Run `./generate_docs.sh` from `bash`.
