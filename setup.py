from setuptools import setup, find_packages


# Function to convert simple ETS component names and versions to a requirements
# spec that works for both development builds and stable builds.
def gendeps(list):
    return ['%s >=%s.dev, <=%s.dev' % (p,min,max) for p,min,max in list]

# Declare our installation requirements.
install_requires = gendeps([
    ("enthought.pyface", "2.0b1", "3"),
    ("enthought.traits", "2.0b1", "3"),
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
