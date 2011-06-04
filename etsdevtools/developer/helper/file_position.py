#-------------------------------------------------------------------------------
#
#  Defines the FilePosition class, a plugin interchange object that defines
#  a specified location within a file.
#
#  Written by: David C. Morrill
#
#  Date: 07/13/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from os.path \
    import basename

from traits.api \
    import HasPrivateTraits, Any, File, Int, Property

#-------------------------------------------------------------------------------
#  'FilePosition' class:
#-------------------------------------------------------------------------------

class FilePosition ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The logical name of the file fragment:
    name = Property

    # The name of the file:
    file_name = File

    # The line number within the file:
    line = Int

    # The number of lines within the file (starting at 'line').
    # A value of -1 means the entire file:
    lines = Int( -1 )

    # The column number within the line:
    column = Int

    # An object associated with this file:
    object = Any

    #---------------------------------------------------------------------------
    #  Implementation of the 'name' property:
    #---------------------------------------------------------------------------

    def _get_name ( self ):
        if self._name is not None:
            return self._name

        return basename( self.file_name )

    def _set_name ( self, name ):
        self._name = name

