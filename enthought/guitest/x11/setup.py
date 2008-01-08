#!/usr/bin/env python
from os.path import join
import sys

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('x11',parent_package,top_path)
    x11_info = config.get_info('x11')
    if x11_info:
        x11_info['libraries'].extend(["Xtst", "Xext", "stdc++"])
    
    guitest_wrap_cxx = config.paths('guitest_wrap.cxx')[0]
    def get_guitest_wrap_cxx(extension, build_dir):
        if x11_info and sys.platform != 'darwin':
            return guitest_wrap_cxx
        print 'No %s will be built for this platform.' % (extension.name)
        return None
    config.add_extension('_guitest',
                         [get_guitest_wrap_cxx],
                         depends = ['*.h','*.c','*.i','guitest_wrap.cxx'],
                         **x11_info)
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(configuration=configuration)
