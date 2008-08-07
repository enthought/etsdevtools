#!/usr/bin/env python
#
# Copyright (c) 2008 by Enthought, Inc.
# All rights reserved.
#

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
- **Gotcha**: A profiling tool based on the Hotshot profiler, which uses
  Chaco for plotting profile data. Can be used as an Envisage plug-in.
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


# NOTE: Setuptools must be imported BEFORE numpy.distutils or else things do
# not work!
from setuptools import find_packages
from setuptools.command.develop import develop

from distutils import log
from distutils.command.build import build as distbuild
from make_docs import HtmlBuild
from numpy.distutils.core import setup
from pkg_resources import DistributionNotFound, parse_version, require, \
    VersionConflict
import os
import zipfile

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
packages = find_packages(exclude=config['packages'] + ['docs', 'examples'])
config['packages'] += packages


# Functions to generate docs from sources when building the project.
def generate_docs():
    """ If sphinx is installed, generate docs.
    """
    doc_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docs')
    source_dir = os.path.join(doc_dir, 'source')
    html_zip = os.path.join(doc_dir,  'html.zip')
    dest_dir = doc_dir

    required_sphinx_version = "0.4.1"
    sphinx_installed = False
    try:
        require("Sphinx>=%s" % required_sphinx_version)
        sphinx_installed = True
    except (DistributionNotFound, VersionConflict):
        log.warn('Sphinx install of version %s could not be verified.'
            ' Trying simple import...' % required_sphinx_version)
        try:
            import sphinx
            if parse_version(sphinx.__version__) < parse_version(
                required_sphinx_version):
                log.error("Sphinx version must be >=" + \
                    "%s." % required_sphinx_version)
            else:
                sphinx_installed = True
        except ImportError:
            log.error("Sphnix install not found.")

    if sphinx_installed:
        log.info("Generating %s documentation..." % INFO['name'])
        docsrc = source_dir
        target = dest_dir

        try:
            build = HtmlBuild()
            build.start({
                'commit_message': None,
                'doc_source': docsrc,
                'preserve_temp': True,
                'subversion': False,
                'target': target,
                'verbose': True,
                'versioned': False
                }, [])
            del build

        except:
            log.error("The documentation generation failed.  Falling back to "
                "the zip file.")

            # Unzip the docs into the 'html' folder.
            unzip_html_docs(html_zip, doc_dir)
    else:
        # Unzip the docs into the 'html' folder.
        log.info("Installing %s documentaion from zip file.\n" % INFO['name'])
        unzip_html_docs(html_zip, doc_dir)

def unzip_html_docs(src_path, dest_dir):
    """ Given a path to a zipfile, extract its contents to a given 'dest_dir'.
    """
    file = zipfile.ZipFile(src_path)
    for name in file.namelist():
        cur_name = os.path.join(dest_dir, name)
        if not name.endswith('/'):
            out = open(cur_name, 'wb')
            out.write(file.read(name))
            out.flush()
            out.close()
        else:
            if not os.path.exists(cur_name):
                os.mkdir(cur_name)
    file.close()

class my_develop(develop):
    def run(self):
        develop.run(self)
        generate_docs()

class my_build(distbuild):
    def run(self):
        distbuild.run(self)
        generate_docs()


# The actual setup call.
setup(
    author = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    classifiers = [c.strip() for c in """\
        Development Status :: 4 - Beta
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
        'develop': my_develop,
        'build': my_build
        },
    dependency_links = [
        'http://code.enthought.com/enstaller/eggs/source',
        ],
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
    tests_require = [
        'nose >= 0.10.3',
        ],
    test_suite = 'nose.collector',
    url = 'http://code.enthought.com/projects/ets_dev_tools.php',
    version = INFO['version'],
    zip_safe = False,
    **config
    )
