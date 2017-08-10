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

Installation (short)
--------------------

.. code:: bash

    pip install perseuspy

Updating to the latest version
------------------------------

.. code:: bash

    pip install --upgrade perseuspy

Installation (Windows long)
---------------------------
First open a terminal by searching for `cmd.exe` in the start menu. Here we can easily
check if all required programs are installed.

#. Check to see if the `pip` executable is already available.
   ::

      pip install perseuspy

   If there is no error you are already done. If it fails, continue with the next steps.
#. Navigate to the installation directory of your `Python` installation. If it is installed
   e.g. `D:/Programs/Python/` we would first change the drive letter (maybe unnecessary)
   and then go to the installation directory.
   ::

       D:
       cd Programs/Python

   Now we should be able to run `python` from the command line.
   ::
       
       python.exe --version

   This should print the installed version of python
#. Navigate to the `Scripts` directory and run the installation
   ::

       cd Scripts
       pip install perseuspy
#. Test the installation by navigating back to the `Python` folder and trying to import `perseuspy`.
   ::

       cd ..
       python.exe

   Now you should be inside the `python` interpreter. Check the installation by running.
   ::

       import perseuspy

   If the command doesn't produce any error you can exit `python` by pressing `CTRL+c`.
#. Add `python` to your `PATH` (optional). Makes it easier for Perseus to find the Python
   installation. There are many resources on how to add programs to the `PATH` available online.
#. To update you installation to the latest version of `perseuspy` simply add `--upgrade` to the
   installation command: `pip install --upgrade perseuspy`.

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

Generating the documentation
----------------------------
Run `./generate_docs.sh` from `bash`.
