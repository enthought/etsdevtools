#-------------------------------------------------------------------------------
#
#  Defines a WatchedFileName interface which allows a plugin to easily
#  monitor its 'file_name' trait (defined by the interface) for external
#  changes.
#
#  Written by: David C. Morrill
#
#  Date: 07/15/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasPrivateTraits, File

from enthought.developer.services.file_watch \
    import file_watch

from enthought.developer.helper.read_file \
    import read_file

#-------------------------------------------------------------------------------
#  'WatchedFileName' interface:
#-------------------------------------------------------------------------------

class WatchedFileName ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The file_name being watched:
    watched_file_name = File

    #---------------------------------------------------------------------------
    #  Handles the 'watched_file_name' trait being changed:
    #---------------------------------------------------------------------------

    def _watched_file_name_changed ( self, old, new ):
        """ Handles the 'watched_file_name' trait being changed.
        """
        if old != '':
            file_watch.watch( self.watched_file_name_updated, old,
                              remove = True )
        if new != '':
            file_watch.watch( self.watched_file_name_updated, new )
        self.watched_file_name_updated( new )

    #---------------------------------------------------------------------------
    #  Handles an update to the specified file:
    #---------------------------------------------------------------------------

    def watched_file_name_updated ( self, file_name ):
        self.watched_file_name_data( read_file( file_name ) )

    #---------------------------------------------------------------------------
    #  Handles new data being read from an updated file:
    #---------------------------------------------------------------------------

    def watched_file_name_data ( self, data ):
        """ Handles new data being read from an updated file.
        """
        pass

