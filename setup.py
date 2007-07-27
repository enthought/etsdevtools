from setuptools import setup, find_packages


# Function to convert simple ETS project names and versions to a requirements
# spec that works for both development builds and stable builds.  Allows
# a caller to specify a max version, which is intended to work along with
# Enthought's standard versioning scheme -- see the following write up:
#    https://svn.enthought.com/enthought/wiki/EnthoughtVersionNumbers
def etsdep(p, min, max=None, literal=False):
    require = '%s >=%s.dev' % (p, min)
    if max is not None:
        if literal is False:
            require = '%s, <%s.dev' % (require, max)
        else:
            require = '%s, <%s' % (require, max)
    return require


# Declare our ETS project dependencies.
PYFACE = etsdep('enthought.pyface', '2.0b1')
TRAITS_UI = etsdep('enthought.traits[ui]', '2.0b1')


setup(
    author = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    description = 'Frame Based Inspector - Traits based debugging tool',
    extras_require = {
        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            ],
        },
    license = 'BSD',
    include_package_data = True,
    install_requires = [
        PYFACE,
        TRAITS_UI,
        ],
    name = 'enthought.debug',
    namespace_packages = [
        "enthought",
        ],
    packages = find_packages(),
    tests_require = [
        'nose >= 0.9',
        ],
    test_suite = 'nose.collector',
    url = 'http://code.enthought.com/ets',
    version = '2.0b2',
    zip_safe = False,
    )
