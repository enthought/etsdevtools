from setuptools import find_packages
from numpy.distutils.core import setup


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


# Function to convert simple ETS project names and versions to a requirements
# spec that works for both development builds and stable builds.  Allows
# a caller to specify a max version, which is intended to work along with
# Enthought's standard versioning scheme -- see the following write up:
#    https://svn.enthought.com/enthought/wiki/EnthoughtVersionNumbers
def etsdep(p, min, max=None, literal=False):
    require = '%s >=%s.dev' % (p, min)
    if max is not None:
        if literal is False:
            require = '%s, <%s.a' % (require, max)
        else:
            require = '%s, <%s' % (require, max)
    return require


# Declare our ETS project dependencies.
APPTOOLS = etsdep('AppTools', '3.0.0b1')
#CHACO_WX = etsdep('Chaco[wx]', '3.0.0b1') - gotcha had this, do we really need it?
#ENABLE_WX = etsdep('Enable[wx]', '3.0.0b1') - gotcha had this, do we really need it?
ENTHOUGHTBASE = etsdep('EnthoughtBase', '3.0.0b1')
ENVISAGECORE = etsdep('EnvisageCore', '3.0.0b1')
TRAITSBACKENDQT = etsdep('TraitsBackendQt', '3.0.0b1')
TRAITSBACKENDWX = etsdep('TraitsBackendWX', '3.0.0b1')
TRAITSGUI_DOCK = etsdep('TraitsGUI[dock]', '3.0.0b1')
TRAITS_UI = etsdep('Traits[ui]', '3.0.0b1')


setup(
    author = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    dependency_links = [
        'http://code.enthought.com/enstaller/eggs/source',
        ],
    description = 'Enthought\'s Development Tools',
    entry_points = {
        'console_scripts': [
            'endo = enthought.endo.scripts.endo:main',
            'endo-readstate = enthought.endo.scripts.readstate:main',
            'ets_endo = enthought.endo.scripts.ets_endo:main',
            'marathon = enthought.testing.marathon:main'
            ]
        },
    extras_require = {
        'plugin': [
            ENVISAGECORE,
            ],
        'qt': [
            TRAITSBACKENDQT,
            ],
        'wx': [
            TRAITSBACKENDWX,
            ],

        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            'cElementTree',
            'elementtree',
            'nose',
            'testoob',
            ],
        },
    include_package_data = True,
    install_requires = [
        APPTOOLS,
        ENTHOUGHTBASE,
        TRAITSGUI_DOCK,
        TRAITS_UI,
        ],
    license = 'BSD',
    name = 'DevTools',
    namespace_packages = [
        'enthought',
        ],
    packages = find_packages(exclude=['docs', 'examples']),
    tests_require = [
        'nose >= 0.9',
        ],
    test_suite = 'nose.collector',
    url = 'http://code.enthought.com/ets',
    version = '3.0.0b1',
    zip_safe = False,
    **configuration().todict()
    )

