#!/usr/bin/env python

import os

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('guitest',parent_package,top_path)
    
    config.add_subpackage('x11')
    config.add_subpackage('win32')
    return config

