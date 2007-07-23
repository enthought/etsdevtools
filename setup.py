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
    ("enthought.traits[ui]", "2.0b1"),
    ])
print 'install_requires:\n\t%s' % '\n\t'.join(install_requires)
test_requires = [
    "nose >= 0.9, ",
    ] + etsdeps([
    ])
print 'test_requires:\n\t%s' % '\n\t'.join(test_requires)


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
    install_requires = install_requires,
    name = 'enthought.debug',
    namespace_packages = [
        "enthought",
        ],
    packages = find_packages(),
    tests_require = test_requires,
    test_suite = 'nose.collector',
    url = 'http://code.enthought.com/ets',
    version = '2.0b2',
    zip_safe = False,
)
