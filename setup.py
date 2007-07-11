from setuptools import setup, find_packages


# Function to convert simple ETS component names and versions to a requirements
# spec that works for both development builds and stable builds.  This relies
# on the Enthought's standard versioning scheme -- see the following write up:
#    https://svn.enthought.com/enthought/wiki/EnthoughtVersionNumbers
def etsdeps(list):
    return ['%s >=%s.dev, <%s.a' % (p,ver,int(ver[:1])+1) for p,ver in list]


# Declare our installation requirements.
install_requires = etsdeps([
    ("enthought.pyface", "2.0b1"),
    ("enthought.traits", "2.0b1"),
    ])
print 'install_requires:\n\t%s' % '\n\t'.join(install_requires)


setup(
    name = 'enthought.debug',
    version = '2.0b2',
    description  = 'Frame Based Inspector - Traits based debugging tool',
    author       = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    url          = 'http://code.enthought.com/ets',
    license      = 'BSD',
    zip_safe     = False,
    packages = find_packages(),
    include_package_data = True,
    install_requires = install_requires,
    extras_require = {
        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
        ],
    },
    namespace_packages = [
        "enthought",
    ],
)
