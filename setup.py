from setuptools import setup, find_packages

setup(
    name = 'enthought.debug',
    version = '2.0.1b1',
    description  = 'Frame Based Inspector - Traits based debugging tool',
    author       = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    url          = 'http://code.enthought.com/ets',
    license      = 'BSD',
    zip_safe     = False,
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        "enthought.envisage >=2.0b1, <3",
        "enthought.logger >=2.0b1, <3",
        "enthought.pyface >=2.0b1, <3",
        "enthought.traits >=2.0b1, <3",
    ],
    namespace_packages = [
        "enthought",
    ],
)
