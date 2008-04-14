###########################################################################
# File:    namespace.py
# Project: docutils
# Date:    2005-06-13
# Author:  David Baer
# 
# Description:
# 
# 
###########################################################################

"""Basic namespace architecture

All of the documented objects from Python have an associated namespace,
so that it is possible to link to related objects -- for example, base
classes, or functions called in attribute/trait definitions.

Here is the basic functionality to make this happen."""

from sets import Set

# local imports
from util import alpha_sort

class Namespace:
    """
    A namespace 
    """
    def __init__(self, parent = None, name = ''):
        # outer namespace (e.g. module namespace for a class)
        self.parent = parent

        # optional namespace name
        self.name = name

        # used for identifier bindings
        self.id_map = { }

    def bind(self, identifier, value):
        """
        bind identifier with a value
        """
        self.id_map[identifier] = value

    def copy(self, other_namespace):
        """
        copy other namespace entirely
        """
        self.id_map.update(other_namespace.id_map)

    def resolve(self, identifier):
        """
        return the construct to which identifier is bound,
               or None if not found
        """
        # first, try to resolve locally
        if self.id_map.has_key(identifier):
            return self.id_map[identifier]

        # if identifier contains a dot, try to resolve partial name
        elif identifier.find('.') != -1:
            # give preference to most specific name
            id_parts = identifier.split('.')
            i = len(id_parts) - 1
            while i > 0:
                left = '.'.join(id_parts[:i])
                right = '.'.join(id_parts[i:])

                if self.id_map.has_key(left):
                    result = self.id_map[left].resolve(right)
                    if result is not None:
                        return result

                # step backward
                i -= 1
            
        # if not locally available, try parent namespace
        elif self.parent is not None:
            return self.parent.resolve(identifier)

        # if everything fails, return None
        return None

    def index(self):
        "complete recursive index, including sub-namespaces"
        result = { }
        result.update(self.id_map)
        for key in self.id_map.keys():
            d = self.id_map[key].index()
            d = dict([ (key + '.' + k, v) for k, v in self.id_map[key].id_map.items() ])
            result.update(d)

        return result

    def get_objects(self):
        "index accessible in this namespace"
        result = self.id_map.items()
        alpha_sort(result)

        return result
            
        

