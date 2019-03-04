perseuspy README
================

.. image:: https://readthedocs.org/projects/perseuspy/badge/?version=latest
    :target: http://perseuspy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. sphinx-inclusion-marker-do-not-remove

.. image:: https://travis-ci.org/jdrudolph/perseuspy.svg?branch=master
    :target: https://travis-ci.org/jdrudolph/perseuspy

This repository contains the source code of the ``perseuspy`` software package.
``perseuspy`` contains convenience functions which allow for faster and easier development
of plugins for `Perseus <https://maxquant.org/perseus>`_ in the Python programming language.
This page contains installation instructions and developer information on ``perseuspy``, for high-level information please
refer to the manuscript listed below.

``perseuspy`` was designed to work in conjunction with the `PluginInterop <https://github.com/jdrudolph/PluginInterop>`_
plugin, but can also be used stand-alone.

Citation
--------

If you use ``perseuspy`` in your projects, please cite

Rudolph, J D and Cox, J 2018, *A network module for the Perseus software for computational proteomics facilitates proteome interaction graph analysis* `doi:10.1101/447268 <https://doi.org/10.1101/447268>`_.

Installation
------------
``perseuspy`` can be installed directly from `pip`. If you are new to Python, more detailed installation instructions for windows are provided below.

.. code:: bash

    pip install perseuspy

Developing plugins
==================

Perseus provides activities to call Python scripts from within the workflow via
`PluginInterop <https://github.com/jdrudolph/PluginInterop>`_, e.g. `Matrix => Python`.
Developing a plugin therefore translates to writing a Python script that follows
a small set of conventions. By adhering to these conventions, Perseus will be
able to successfully communicate with R and transfer inputs and results between
the programs. ``perseuspy`` provides the neccessary functions to make plugin development
in Python easy and straight forward.

Matrix plugin
-------------
This example Python script extracts the first 15 rows from the matrix. While its functionality
is very simple. It can serve as a starting point for more extensive scripts.

.. code:: python

    import sys
    from perseuspy import pd
    from perseuspy.parameters import *
    _, infile, outfile = sys.argv # read arguments from the command line
    df = pd.read_perseus(infile) # read the input matrix into a pandas.DataFrame
    df2 = df.head(15) # keep only the first 15 rows of the table
    df2.to_perseus(outfile) # write pandas.DataFrame in Perseus txt format
    
Network plugin
--------------
The following snippet can be used as a starting point for network analyses.

.. code:: python

    import sys
    from perseuspy import nx, pd, read_networks, write_networks
    _, infolder, outfolder = sys.argv # read arguments from the command line
    networks_table, networks = read_networks(infolder) # networks in tabular form
    graphs = nx.from_perseus(networks_table, networks) # graphs as networkx objects
    # perform some analysis
    _networks_table, _networks = nx.to_perseus(graphs) # convert back into tabular form
    write_networks(tmp_dir, networks_table, networks) # write to folder


Updating to the latest version
------------------------------

.. code:: bash

    pip install --upgrade perseuspy

Installation (Windows long)
---------------------------
First open a terminal by searching for ``cmd.exe`` in the start menu. Here we can easily
check if all required programs are installed.

#. Check to see if the ``pip`` executable is already available.
   ::

      pip install perseuspy

   If there is no error you are already done. If it fails, continue with the next steps.
#. Navigate to the installation directory of your Python installation. If it is installed
   e.g. ``D:/Programs/Python/`` we would first change the drive letter (maybe unnecessary)
   and then go to the installation directory.
   ::

       D:
       cd Programs/Python

   Now we should be able to run ``python`` from the command line.
   ::
       
       python.exe --version

   This should print the installed version of python
#. Navigate to the ``Scripts`` directory and run the installation
   ::

       cd Scripts
       pip install perseuspy

   If you want to upgrade you installation, run
   ::

       pip install --upgrade perseuspy

#. Test the installation by navigating back to the Python folder and trying to import ``perseuspy``.
   ::

       cd ..
       python.exe

   Now you should be inside the ``python`` interpreter. Check the installation by running.
   ::

       import perseuspy

   If the command doesn't produce any error you can exit ``python`` by pressing `CTRL+c`.
#. Add ``python`` to your ``PATH`` (optional, recommended). Makes it easier for Perseus to find the Python
   installation. There are many resources on how to add programs to the ``PATH`` available online. No description
   is provided here since instructions are specific to the version of Windows that is used.

Usage
------------
You can use ``perseuspy`` just like any other python module.

.. code:: python

    # import a monkey-patched version of pandas
    from perseuspy import pd
    df = pd.read_perseus('matrix1.txt')
    df2 = df.dropna()
    df2.to_perseus('matrix2.txt')


Generating the developer documentation
--------------------------------------
Run ``./generate_docs.sh`` from ``bash``.

Licensing and Contributions
---------------------------
``perseuspy`` is licensed under the MIT lisence.
Contributions are welcome! If you are interested in contributing to code or documentation,
please read `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.
