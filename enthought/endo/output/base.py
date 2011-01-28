###########################################################################
# File:    base.py
# Project: docutils
# Date:    2005-07-11
# Author:  David Baer
#
# Description:
#  Base class for output backends
#
###########################################################################

"Basic output architecture"

import sys

sys.path.append('..')
from enthought.endo.namespace import Namespace

class FormattingException(Exception): pass

class OutputBase:
    """Base class for output backends
    """

    def __init__(self, options):
        """Class initializer

        options : command line options"""
        self.options = options
        self.modules = [ ]
        self.modules_by_name = { }
        self.package_namespace = Namespace(name = options.package)

    def add_module(self, module):
        "Add a parsed module (docobjects.Module) to be documented"
        self.modules.append(module)
        self.modules_by_name[module.abs_name] = module
        self.package_namespace.bind(module.abs_name, module)

        # add module to parent as submodule, if parent present
        dot = module.abs_name.rfind('.')
        if dot != -1:
            parent_name = module.abs_name[:dot]
            if self.modules_by_name.has_key(parent_name):
                self.modules_by_name[parent_name].add_sub_module(module)

    def resolve_imports(self):
        "Resolve dangling imports after all modules scanned"
        for module in self.modules:
            module.resolve_imports(self.modules_by_name)

    def write_output(self):
        "Generate documentation"
        self.resolve_imports()
        self.generate()

    def generate(self):
        pass



