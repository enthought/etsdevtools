#-------------------------------------------------------------------------------
#
#  Defines the ObjectAdapterBase class used as the base class for all browser
#  adapter classes.
#
#  Written by: David C. Morrill
#
#  Date: 06/17/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasPrivateTraits, File, Code, Property

from enthought.pyface.dock.api \
    import IDockUIProvider

#-------------------------------------------------------------------------------
#  'ObjectAdapterBase' class:
#-------------------------------------------------------------------------------

class ObjectAdapterBase ( HasPrivateTraits, IDockUIProvider ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The file name the object definition is contained in:
    file_name = File

    # The source code containing the object definition:
    source = Property( Code )

#-- Property Implementations ---------------------------------------------------

    def _get_source ( self ):
        return self._get_file_contents( 'source', self.file_name )

#-- Private Methods ------------------------------------------------------------

    def _get_file_contents ( self, name, file_name ):
        """ Defines a property getter whose value is the contents of a
            specified file name.
        """
        contents = getattr( self, '_' + name, None )
        if contents is None:
            fh = None
            try:
                fh = file( file_name, 'rb' )
                contents = fh.read()
            except:
                contents = ''
                if fh is not None:
                    try:
                        fh.close()
                    except:
                        pass
            setattr( self, '_' + name, contents )

        return contents

