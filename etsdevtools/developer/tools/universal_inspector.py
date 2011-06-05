#-------------------------------------------------------------------------------
#
#  Universal Inspector plugin
#
#  Written by: David C. Morrill
#
#  Date: 06/25/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from os.path \
    import basename

from cPickle \
    import load

from cStringIO \
    import StringIO

from traits.api \
    import HasPrivateTraits, Any, Int, Str, Code, List, Range, Property, Bool, \
           Title

from traitsui.api \
    import View, VGroup, HGroup, Item, ListEditor, DNDEditor, ValueEditor, \
           CodeEditor

from etsdevtools.developer.helper.themes \
    import TTitle

from apptools.io.file \
    import File

from pyface.timer.api \
    import do_later

from etsdevtools.developer.api \
    import HasPayload, FilePosition, read_file, file_watch

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# All valid text characters:
text_characters = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                   '0123456789`~!@#$%^&*()-_=+[]{}\\|\'";:,<.>/?\r\n\t ')

#-------------------------------------------------------------------------------
#  'UniversalInspector' plugin:
#-------------------------------------------------------------------------------

class UniversalInspector ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Universal Inspector' )

    # The persistence id for this object:
    id = Str( 'etsdevtools.developer.tools.universal_inspector.state',
              save_state_id = True )

    # Maximum number of open inspectors allowed:
    max_inspectors = Range( 1, 50, 50, mode = 'spinner', save_state = True )

    # The current item being inspected:
    item = Any( droppable = 'Drop a Python object or value here.',
                connect   = 'both' )

    # Current list of items being inspected:
    inspectors = List

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( 'inspectors@',
              show_label = False,
              editor     = ListEditor( use_notebook = True,
                                       deletable    = True,
                                       page_name    = '.name',
                                       export       = 'DockWindowShell',
                                       dock_style   = 'tab' )
        )
    )

    options = View(
        Item( 'max_inspectors',
              label = 'Maximum number of open inspectors',
              width = -50
        ),
        title   = 'Universal Inspector Options',
        id      = 'etsdevtools.developer.tools.universal_inspector.options',
        buttons = [ 'OK', 'Cancel' ]
    )

    #---------------------------------------------------------------------------
    #  Handles the 'max_inspectors' trait being changed:
    #---------------------------------------------------------------------------

    def _max_inspectors_changed ( self, max_inspectors ):
        """ Handles the 'max_inspectors' trait being changed.
        """
        delta = len( self.inspectors ) - max_inspectors
        if delta > 0:
            del self.inspectors[ : delta ]

    #---------------------------------------------------------------------------
    #  Handles the 'item' trait being changed:
    #---------------------------------------------------------------------------

    def _item_changed ( self, item ):
        """ Handles the 'item' trait being changed.
        """
        # Check to see if it is a list of File objects, which represent files
        # dropped onto the view from an external source (like MS Explorer):
        if isinstance( item, list ) and (len( item ) > 0):
            for an_item in item:
                if not isinstance( an_item, File ):
                    break
            else:
                for an_item in item:
                    self._item_changed( an_item )
                return

        # Set up the default values:
        name  = full_name = ''
        line  = 0
        lines = -1

        # Extract the file name from a File object:
        if isinstance( item, File ):
            item = item.absolute_path

        # Handle the case of an item which contains a payload:
        elif isinstance( item, HasPayload ):
            name      = item.payload_name
            full_name = item.payload_full_name
            item      = item.payload

        # Handle the case of a file position, which has a file name and a
        # possible starting line and range of lines:
        if isinstance( item, FilePosition ):
            name  = item.name
            line  = item.line
            lines = item.lines
            item  = item.file_name

        # Only create an inspector if there actually is a valid item:
        if item is not None:
            inspector = None

            # If it is a string value, check to see if it is a valid file name:
            if isinstance( item, basestring ):
                data = read_file( item, 'r' )
                if data is not None:
                    if name == '':
                        name      = basename( item )
                        full_name = item
                    try:
                        inspector = ObjectInspector(
                            object    = self._object_from_pickle( data ),
                            name      = name,
                            full_name = full_name )
                    except:
                        try:
                            inspector = ObjectInspector(
                                object    = self._object_from_pickle(
                                                read_file( item ) ),
                                name      = name,
                                full_name = full_name )
                        except:
                            inspector = FileInspector( name      = name,
                                                       line      = line,
                                                       lines     = lines ).set(
                                                       file_name = item )

            # If it is not a file, then it must just be a generic object:
            if inspector is None:
                inspector = ObjectInspector( object    = item,
                                             name      = name,
                                             full_name = full_name )

            inspectors = self.inspectors

            # Make sure the # of inspectors doesn't exceed the maximum allowed:
            if len( inspectors ) >= self.max_inspectors:
                del inspectors[0]

            # Add the new inspector to the list of inspectors (which will
            # cause it to appear as a new notebook page):
            inspectors.append( inspector )

            # Reset the current item to None, so we are ready for a new item:
            do_later( self.set, item = None )

    #-- Private Methods --------------------------------------------------------

    def _object_from_pickle ( self, data ):
        """ Tries the return the objects contained in a 'pickle' buffer.
        """
        buffer = StringIO( data )
        object = [ load( buffer ) ]
        try:
            while True:
                object.append( load( buffer ) )
        except:
            import traceback
            traceback.print_exc()

        if len( object ) == 1:
            object = object[0]

        return object

#-------------------------------------------------------------------------------
#  'ObjectInspector' class:
#-------------------------------------------------------------------------------

class ObjectInspector ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The inspector page name:
    name = Property

    # The inspector's full object name:
    full_name = Property

    # The object being inspected:
    object = Any( draggable = 'Drag the object.' )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View(
        VGroup(
            TTitle( 'full_name' ),
            Item( 'object',    editor = ValueEditor() ),
            show_labels = False
        )
    )

    #---------------------------------------------------------------------------
    #  Implementation of the 'name' property:
    #---------------------------------------------------------------------------

    def _get_name ( self ):
        if self._name != '':
            return self._name

        return '%s [0x%08X]' % ( self.object.__class__.__name__,
                                 id( self.object ) )

    def _set_name ( self, name ):
        self._name = name

    #---------------------------------------------------------------------------
    #  Implementation of the 'full_name' property:
    #---------------------------------------------------------------------------

    def _get_full_name ( self ):
        if self._full_name != '':
            return self._full_name

        return '%s [0x%08X]' % ( self.object.__class__.__name__,
                                 id( self.object ) )

    def _set_full_name ( self, full_name ):
        self._full_name = full_name

#-------------------------------------------------------------------------------
#  'FileInspector' class:
#-------------------------------------------------------------------------------

class FileInspector ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The inspector page name:
    name = Property

    # The name of the file being inspected:
    file_name = Title( draggable = 'Drag the file name.' )

    # The starting line number:
    line = Int

    # The number of lines (start at 'line'):
    lines = Int( -1 )

    # The text being inspected:
    text = Code

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View(
        VGroup(
            Item( 'file_name' ),
            Item( 'text~',
                  editor = CodeEditor( selected_line = 'line' )
            ),
            show_labels = False
        )
    )

    #---------------------------------------------------------------------------
    #  Handles the 'file_name' trait being changed:
    #---------------------------------------------------------------------------

    def _file_name_changed ( self, old_file_name, new_file_name ):
        """ Handles the 'file_name' trait being changed.
        """
        if old_file_name != '':
            file_watch.watch( self._update, old_file_name, remove = True )

        if new_file_name != '':
            file_watch.watch( self._update, new_file_name )
            self._update( new_file_name )

    #---------------------------------------------------------------------------
    #  Updates the view with the contents of the specified file:
    #---------------------------------------------------------------------------

    def _update ( self, file_name ):
        """ Updates the view with the contents of the specified file.
        """
        data = read_file( file_name )
        if data is not None:
            if self.is_text( data ):
                if self.lines > 0:
                    self.text = '\n'.join( data.split( '\n' )
                                [ max( 0, self.line - 1 ):
                                  self.line + self.lines - 1 ] )
                else:
                    self.text = data
            else:
                format    = self.format
                self.text = '\n'.join( [ format( i, data[ i: i + 16 ] )
                                       for i in range( 0, len( data ), 16 ) ] )

    #---------------------------------------------------------------------------
    #  Implementation of the 'name' property:
    #---------------------------------------------------------------------------

    def _get_name ( self ):
        if self._name != '':
            return self._name

        return basename( self.file_name )

    def _set_name ( self, name ):
        self._name = name

    #---------------------------------------------------------------------------
    #  Returns whether a specified buffer contains only valid text characters:
    #---------------------------------------------------------------------------

    def is_text ( self, buffer ):
        """ Returns whether a specified buffer contains only valid text characters.
        """
        for i in range( min( 256, len( buffer ) ) ):
            if not buffer[i] in text_characters:
                return False

        return True

    #---------------------------------------------------------------------------
    #  Formats a binary string of data as a hex encoded string:
    #---------------------------------------------------------------------------

    def format ( self, offset, data ):
        """ Formats a binary string of data as a hex encoded string.
        """
        hb = [ self.hex_bytes( data[ i: i + 4 ] ) for i in range( 0, 16, 4 ) ]
        return ('#%08X  %s %s %s %s  |%s|' % (
                offset, hb[0], hb[1], hb[2], hb[3], self.ascii_bytes( data ) ))

    #---------------------------------------------------------------------------
    #  Returns the hex encoding of a string of up to 4 bytes of data:
    #---------------------------------------------------------------------------

    def hex_bytes ( self, data ):
        return ''.join( [ self.hex_byte( data[ i: i + 1 ] )
                        for i in range( 0, 4 ) ] )

    #---------------------------------------------------------------------------
    #  Returns the hex encoding of a 0 or 1 length string of data:
    #---------------------------------------------------------------------------

    def hex_byte ( self, byte ):
        """ Returns the hex encoding of a 0 or 1 length string of data.
        """
        if len( byte ) == 0:
            return '  '

        return ('%02X' % ord( byte ))

    #---------------------------------------------------------------------------
    #  Returns the ascii encoding of up to 16 bytes of data:
    #---------------------------------------------------------------------------

    def ascii_bytes ( self, data ):
        return ''.join( [ self.ascii_byte( data[ i: i + 1 ] )
                        for i in range( 0, 16 ) ] )

    #---------------------------------------------------------------------------
    #  Returns the ascii encoding of a 0 or 1 length string of data:
    #---------------------------------------------------------------------------

    def ascii_byte ( self, byte ):
        """ Returns the hex encoding of a 0 or 1 length string of data.
        """
        if len( byte ) == 0:
            return ' '

        n = ord( byte )
        if 32 <= n <= 127:
            return byte

        return '.'

#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = UniversalInspector()

