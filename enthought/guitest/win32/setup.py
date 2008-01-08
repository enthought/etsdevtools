#!/usr/bin/env python
def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('win32',parent_package,top_path)
    guitest_wrap_cxx = config.paths('guitest_wrap.cxx')[0]
    def get_guitest_wrap_cxx(extension, build_dir):
        import sys
        if sys.platform=='win32': return guitest_wrap_cxx
        print 'No %s will be built for this platform.' % (extension.name)
        return None
    config.add_extension('_guitest',
                         [get_guitest_wrap_cxx],
                         depends = ['*.h','*.cpp','*.i','guitest_wrap.cxx'],
                         libraries = ['gdi32', 'user32'])
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(configuration=configuration)
