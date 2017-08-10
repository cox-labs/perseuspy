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

#. We can check if `git` is installed by typing
   ::
        
        git --version
        
   If the command returns an error, go ahead and install `git <https://git-scm.com/downloads>`_.
   Make sure to select 'Add `git` to `PATH`' during the installation. Now rerunning the
   command above should output the installed version of git.
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
       pip install git+https://github.com/jdrudolph/perseuspy.git
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
