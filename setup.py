from setuptools import setup, find_packages

setup(
    name = 'enthought.debug',
    version = '1.1.0',
    description  = 'Frame Based Inspector - Traits based debugging tool',
    author       = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    url          = 'http://code.enthought.com/ets',
    license      = 'BSD',
    zip_safe     = False,
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        "enthought.traits", 
        "enthought.pyface",
    ],
    namespace_packages = [
        "enthought",
    ],
)
