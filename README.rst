================================================
etsdevtools: tools to support Python development
================================================

http://github.enthought.com/etsdevtools

The etsdevtools project includes a set of packages that can be used during the
development of a software project, for understanding, debugging, testing, and
inspecting code.

- **etsdevtools.debug**: A collection of debugging tools, not to be included
  in production code. NOTE: These tools are functional, but are not being
  developed or supported. They have been mainly superceded by the tools
  in the Enthought Developer Tool Suite.
- **etsdevtools.developer**: A collection of
  utilities, designed to ease the development and debugging of Traits-based
  programs. They can be used as plug-ins to your Envisage application while
  you are developing it, and then removed when you are ready to release it.
- **etsdevtools.endo**: A Traits-aware tool for processing API documentation
  of Python code. It extracts not only docstrings, but also plain comments
  that immediately precede variable assignments (both module-scope variables
  and class attributes).

Prerequisites
-------------

* `Numpy <http://pypi.python.org/pypi/numpy>`_
* `traits <https://github.com/enthought/traits>`_
