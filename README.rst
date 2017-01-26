perseuspy README
===============

.. image:: https://travis-ci.org/jdrudolph/perseuspy.svg?branch=master
    :target: https://travis-ci.org/jdrudolph/perseuspy

Utility and covenience functions for Perseus-python interop.
Building on the `pandas` package.

Installation
------------
Install using pip directly from `github`:

.. code:: bash

    pip install git+https://github.com/jdrudolph/perseuspy.git

Usage
------------

.. code:: python

    # import a monkey-patched version of pandas
    from perseuspy import pd
    df = pd.read_perseus('matrix1.txt')
    df2 = df.dropna()
    df2.to_perseus('matrix2.txt')
