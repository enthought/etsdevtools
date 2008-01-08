###########################################################################
# File:    loader.py
# Project: docutils
# Date:    2005-07-29
# Author:  David Baer
# 
# Description:
# 
# 
###########################################################################

"Template loader agent"

import os
from enthought.endo.template import Template

class TemplateLoader:
    """The template loader is responsible for loading templates.

    A template loaded with the loader will be able to use it to import
    additional templates."""
    def __init__(self, path_list):
        self.path_list = path_list
        self.cache = { }

    def load(self, name):
        if self.cache.has_key(name):
            return self.cache[name]
        paths_to_try = self.path_list

        while len(paths_to_try) > 0:
            path = paths_to_try[0]
            try:
                filename = os.path.join(path, name + '.html')
                f = open(filename, 'rt')
                t = Template(f.read(), file=filename, loader=self)
                f.close()
                self.cache[name] = t
                return t
            except IOError:
                paths_to_try = paths_to_try[1:]
                if len(paths_to_try) == 0:
                    raise

        

