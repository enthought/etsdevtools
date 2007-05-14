import os

minimum_numpy_version = '0.9.7.2467'
def configuration(parent_package='enthought',top_path=None):
    import numpy
    if numpy.__version__ < minimum_numpy_version:
        raise RuntimeError, 'numpy version %s or higher required, but got %s'\
              % (minimum_numpy_version, numpy.__version__)

    from numpy.distutils.misc_util import Configuration
    config = Configuration('debug',parent_package,top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)
                       
    #add the parent __init__.py to allow for importing
    config.add_data_files(('..', os.path.abspath(os.path.join('..','__init__.py'))))                       

    #add the parent __init__.py to allow for importing
    config.add_data_files(('..', os.path.abspath(os.path.join('..','__init__.py'))))
    
    config.add_data_dir('images')

    config.add_data_dir('plugin')
    config.add_subpackage('plugin')

    config.add_data_files('*.txt')

    return config

if __name__ == "__main__":
     from numpy.distutils.core import setup
     setup(version='1.1.0',
           description  = 'Frame Based Inspector - Traits based debugging tool',
           author       = 'Enthought, Inc',
           author_email = 'info@enthought.com',
           url          = 'http://code.enthought.com/ets',
           license      = 'BSD',
           install_requires = ["enthought.traits", "enthought.pyface"],
           zip_safe     = False,
           configuration=configuration)

