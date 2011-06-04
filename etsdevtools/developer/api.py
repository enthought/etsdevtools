#-------------------------------------------------------------------------------
#
#  enthought.developer package core API
#
#  Written by: David C. Morrill
#
#  Date: 07/18/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.developer.helper.trait_defs \
    import TraitValue

from enthought.developer.helper.file_position \
    import FilePosition

from enthought.developer.helper.python_file_position \
    import PythonFilePosition

from enthought.developer.helper.has_payload \
    import HasPayload

from enthought.developer.helper.pickle \
    import get_pickle, set_pickle

from enthought.developer.helper.read_file \
    import read_file

from enthought.developer.helper.saveable \
    import Saveable

from enthought.developer.helper.watched_file_name \
    import WatchedFileName

from enthought.developer.helper.functions \
    import truncate, import_module, import_symbol

from enthought.developer.services.file_watch \
    import file_watch

#-------------------------------------------------------------------------------
#  Helpful functions:
#-------------------------------------------------------------------------------

def develop ( obj_or_class, args = (), traits = {} ):
    """ Provides a simple development environment for developing the specified
        object or class.
    """
    from develop import develop

    develop( obj_or_class, args, traits )

