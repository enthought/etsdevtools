#-------------------------------------------------------------------------------
#
#  etsdevtools.developer package core API
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

from etsdevtools.developer.helper.trait_defs \
    import TraitValue

from etsdevtools.developer.helper.file_position \
    import FilePosition

from etsdevtools.developer.helper.python_file_position \
    import PythonFilePosition

from etsdevtools.developer.helper.has_payload \
    import HasPayload

from etsdevtools.developer.helper.pickle \
    import get_pickle, set_pickle

from etsdevtools.developer.helper.read_file \
    import read_file

from etsdevtools.developer.helper.saveable \
    import Saveable

from etsdevtools.developer.helper.watched_file_name \
    import WatchedFileName

from etsdevtools.developer.helper.functions \
    import truncate, import_module, import_symbol

from etsdevtools.developer.services.file_watch \
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

