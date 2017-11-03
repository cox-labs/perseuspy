Contributing
============

Overview
--------
`perseuspy` follows the standard github workflow.

1. Fork the repository
2. Make changes to your code
3. Make a pull request

Requirements
------------
Every pull request is checked by the continuous integration system.
Pull requests generally only be merged if they can be build without
errors, and all unit tests pass. Additionally, if the API/documentation
was changed. The `apidoc` documentation has to be updated.

1. Declare requirements in `setup.py`.
2. Test your code and verify correctness by running `python setup.py test`.
3. Generate the documentation.

Coding style and documentation
------------------------------
All public functions and modules should be documented with docstrings `"""docstring"""` in sphinx syntax.
