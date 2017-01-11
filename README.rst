perseuspy README
===============

Utility and covenience functions for Perseus-python interop.
Building on the `pandas` package.

Usage
------------

.. code:: python

    # import a monkey-patched version of pandas
    from perseuspy import pd
    df = pd.read_perseus('matrix1.txt')
    df2 = df.dropna()
    df2.to_perseus('matrix2.txt')
