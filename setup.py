#!/usr/bin/env python
#
# Copyright (c) 2008-2009 by Enthought, Inc.
# All rights reserved.


"""
Enthought tools to support Python development.

The ETSDevTools project includes a set of packages that can be used during the
development of a software project, for understanding, debugging, testing, and
inspecting code.

- **Enthought Developer Tool Suite** (enthought.developer): A collection of
  utilities, designed to ease the development and debugging of Traits-based
  programs. They can be used as plug-ins to your Envisage application while
  you are developing it, and then removed when you are ready to release it.
- **Endo**: A Traits-aware tool for processing API documentation of Python
  code. It extracts not only docstrings, but also plain comments that
  immediately precede variable assignments (both module-scope variables and
  class attributes).
- **enthought.guitest**: A collection of utilities for unit testing user
  interfaces (translation of the Perl X11::GUITest and Win32::GuiTest modules).
- **enthought.testing**: Scripts related to running unit tests, based on
  testoob, and also allowing running test suites in separate processes and
  aggregating the results.
- **enthought.debug**: A collection of debugging tools, not to be included in
  production code. NOTE: These tools are functional, but are not being
  developed or supported. They have been mainly superceded by the tools
  in the Enthought Developer Tool Suite.

Prerequisites
-------------
You must have the following libraries installed before building or installing
ETSDevTools:

* `Numpy <http://pypi.python.org/pypi/numpy/1.1.1>`_ version 1.1.0 or later is
  preferred. Version 1.0.4 will work, but some tests may fail.
* `setuptools <http://pypi.python.org/pypi/setuptools/0.6c8>`_
"""

import traceback
import sys

# NOTE: Setuptools must be imported BEFORE numpy.distutils or else things do
# not work!
import setuptools

import distutils
from distutils import log
import numpy


# FIXME: This works around a setuptools bug which gets setup_data.py metadata
# from incorrect packages. Ticket #1592
#from setup_data import INFO
setup_data = dict(__name__='', __file__='setup_data.py')
execfile('setup_data.py', setup_data)
INFO = setup_data['INFO']


# Pull the description values for the setup keywords from our file docstring.
DOCLINES = __doc__.split("\n")


# Configure python extensions
def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)
    config.set_options(
        ignore_setup_xxx_py=True,
        assume_default_configuration=True,
        delegate_options_to_subpackages=True,
        quiet=True,
    )

    config.add_subpackage('enthought.guitest')
    config.add_subpackage('enthought')

    return config


# Build the full set of packages by appending any found by setuptools'
# find_packages to those discovered by numpy.distutils.
config = configuration().todict()
packages = setuptools.find_packages(exclude=config['packages'] + ['docs',
    'examples'])
config['packages'] += packages


class MyDevelop(setuptools.command.develop.develop):
    def run(self):
        setuptools.command.develop.develop.run(self)
        try:
            self.run_command('build_docs')
        except:
            log.warn("Couldn't build documentation:\n%s" %
                     traceback.format_exception(*sys.exc_info()))



class MyBuild(numpy.distutils.command.build.build):
    def run(self):
        numpy.distutils.command.build.build.run(self)
        try:
            self.run_command('build_docs')
        except:
            log.warn("Couldn't build documentation:\n%s" %
                     traceback.format_exception(*sys.exc_info()))



# The actual setup call.
numpy.distutils.core.setup(
    author = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    classifiers = [c.strip() for c in """\
        Development Status :: 5 - Production/Stable
        Intended Audience :: Developers
        Intended Audience :: Science/Research
        License :: OSI Approved :: BSD License
        Operating System :: MacOS
        Operating System :: Microsoft :: Windows
        Operating System :: OS Independent
        Operating System :: POSIX
        Operating System :: Unix
        Programming Language :: Python
        Topic :: Scientific/Engineering
        Topic :: Software Development
        Topic :: Software Development :: Libraries
        """.splitlines() if len(c.strip()) > 0],
    cmdclass = {
        'develop': MyDevelop,
        'build': MyBuild
        },
    description = DOCLINES[1],
    entry_points = {
        'console_scripts': [
            'endo = enthought.endo.scripts.endo:main',
            'endo-readstate = enthought.endo.scripts.readstate:main',
            'ets_endo = enthought.endo.scripts.ets_endo:main',
            'marathon = enthought.testing.marathon:main'
            ]
        },
    extras_require = INFO['extras_require'],
    include_package_data = True,
    install_requires = INFO['install_requires'],
    license = 'BSD',
    long_description = '\n'.join(DOCLINES[3:]),
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    name = INFO['name'],
    namespace_packages = [
        'enthought',
        ],
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    setup_requires = 'setupdocs>=1.0',
    tests_require = [
        'nose >= 0.10.3',
        ],
    test_suite = 'nose.collector',
    url = 'http://code.enthought.com/projects/ets_dev_tools.php',
    version = INFO['version'],
    zip_safe = False,
    **config
    )

