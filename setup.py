# Copyright (c) 2008-2011 by Enthought, Inc.
# All rights reserved.
from os.path import join

# NOTE: Setuptools must be imported BEFORE numpy.distutils or else things do
# not work!
import setuptools

import numpy


info = {}
execfile(join('etsdevtools', '__init__.py'), info)


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

    config.add_subpackage('etsdevtools')

    return config


# Build the full set of packages by appending any found by setuptools'
# find_packages to those discovered by numpy.distutils.
config = configuration().todict()
packages = setuptools.find_packages(exclude=config['packages'] +
                                    ['docs', 'examples'])
config['packages'] += packages


# The actual setup call.
numpy.distutils.core.setup(
    name = 'etsdevtools',
    version = info['__version__'],
    author = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    url = 'http://code.enthought.com/projects/ets_dev_tools.php',
    download_url = ('http://www.enthought.com/repo/ets/ETSDevTools-%s.tar.gz'
                    % info['__version__']),
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
    description = 'tools to support Python development',
    long_description = open('README.rst').read(),
    entry_points = {
        'console_scripts': [
            'endo = etsdevtools.endo.scripts.endo:main',
            'endo-readstate = etsdevtools.endo.scripts.readstate:main',
            'ets_endo = etsdevtools.endo.scripts.ets_endo:main',
            ]
        },
    include_package_data = True,
    package_data = {'etsdevtools': ['endo/data/*.*']},
    install_requires = info['__requires__'],
    license = 'BSD',
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    zip_safe = False,
    **config
)
