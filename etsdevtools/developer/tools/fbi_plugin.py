#-------------------------------------------------------------------------------
#
#  FBI plugin for handling exceptions that occur while running an Envisage
#  application.
#
#  Written by: David C. Morrill
#
#  Date: 10/18/2005
#
#  (c) Copyright 2005 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import sys

from traits.api \
    import push_exception_handler

from envisage.api \
    import Plugin

from etsdevtools.developer.helper.fbi \
    import enable_fbi, fbi

#-------------------------------------------------------------------------------
#  'FBIPlugin' class:
#-------------------------------------------------------------------------------

class FBIPlugin ( Plugin ):
    """ FBIPython plugin. """

    #---------------------------------------------------------------------------
    #  'Plugin' interface:
    #---------------------------------------------------------------------------

    def start ( self ):
        """ Starts the plugin.
        """
        # Tell the FBI to wiretap all unauthorized exceptions:
        enable_fbi()
        # FIXME: Should this code be removed? enable_fbi calls
        # push_exception_handler with locked=True, and therefore, including
        # this code raises an error about the Traits notification exception
        # handler being locked.
        #push_exception_handler( handler = lambda obj, name, old, new: fbi(),
        #                        locked  = False,
        #                        main    = True )

