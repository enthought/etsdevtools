#-------------------------------------------------------------------------------
#
#  Traceback Viewer plugin
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

import re
import wx
import sys

from os.path \
    import basename, dirname

from traits.api \
    import HasPrivateTraits, Any, Constant, File, Int, List, Code, Instance, \
           Str, Property

from traitsui.api \
    import View, VGroup, HGroup, Item, TableEditor

from traitsui.table_column \
    import ObjectColumn

from pyface.wx.clipboard \
    import clipboard

from pyface.image_resource \
    import ImageResource

from etsdevtools.developer.features.api \
    import CustomFeature

from etsdevtools.developer.api \
    import FilePosition

from etsdevtools.developer.helper.themes \
    import TTitle

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

file_pat       = re.compile( r'^\s*File "(.*?)", line\s*(\d*),\s*in\s*(.*)' )
file_begin_pat = re.compile( r'^\s*File "' )

#-------------------------------------------------------------------------------
#  'TracebackEntry' class:
#-------------------------------------------------------------------------------

class TracebackEntry ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Traits definitions:
    #---------------------------------------------------------------------------

    # The file associated with the traceback entry:
    file_name = File

    # The base file name (minus path):
    base_name = Property

    # The file name path:
    path_name = Property

    # The line number within the file:
    line = Int

    # The source code line:
    source = Code

    # The function/method name:
    name = Str

    #-- Property Implementations -----------------------------------------------

    def _get_base_name ( self ):
        return basename( self.file_name )

    def _get_path_name ( self ):
        return dirname( self.file_name )

#-------------------------------------------------------------------------------
#  Traceback table editor definition:
#-------------------------------------------------------------------------------

traceback_table_editor = TableEditor(
    columns = [ ObjectColumn( name     = 'base_name',
                              label    = 'Base Name',
                              editable = False ),
                ObjectColumn( name     = 'line',
                              editable = False,
                              horizontal_alignment = 'center' ),
                ObjectColumn( name     = 'name',
                              label    = 'Caller',
                              editable = False ),
                ObjectColumn( name     = 'source',
                              editable = False ) ],
    other_columns = [
                ObjectColumn( name     = 'file_name',
                              label    = 'File Name',
                              editable = False ),
                ObjectColumn( name     = 'path_name',
                              label    = 'Path Name',
                              editable = False ) ],
    auto_size          = False,
    sortable           = False,
    selection_bg_color = 0xFBD391,
    selection_color    = 'black',
    selected           = 'selected'
)

#-------------------------------------------------------------------------------
#  'TracebackViewer' plugin:
#-------------------------------------------------------------------------------

class TracebackViewer ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Traceback Viewer' )

    feature = Instance( CustomFeature, {
                            'image':   ImageResource( 'clipboard' ),
                            'click':   'paste_traceback',
                            'tooltip': 'Click to paste traceback' },
                            custom_feature = True )

    # Connectable form of traceback information:
    buffer = Str( connect = 'to: traceback text' )

    # The exception that occurred:
    exception = Str

    # The current traceback being processed:
    traceback = List( TracebackEntry )

    # The currently selected traceback item:
    selected = Instance( TracebackEntry, allow_none = False )

    # The file position within the currently selected traceback file:
    file_position = Instance( FilePosition,
                        connect   = 'from: file position',
                        draggable = 'Drag current traceback file position.' )

    # The original value of sys.stderr:
    stderr = Any

    # Traceback accumulation buffer:
    lines = List( Str )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        TTitle( 'exception' ),
        Item( 'traceback',
              id         = 'traceback',
              show_label = False,
              editor     = traceback_table_editor
        ),
        id = 'etsdevtools.developer.tools.traceback_viewer'
    )

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, **traits ):
        """ Initializes the object.
        """
        super( TracebackViewer, self ).__init__( **traits )
        self.stderr, sys.stderr = sys.stderr, self

    #---------------------------------------------------------------------------
    #  Handles 'write' calls to stderr:
    #---------------------------------------------------------------------------

    def write ( self, buffer ):
        """ Handles 'write' calls to stderr.
        """
        self.stderr.write( buffer )
        lines = buffer.split( '\n' )
        n     = len( self.lines )
        if n == 0:
            for i, line in enumerate( lines ):
                if line == 'Traceback (most recent call last):':
                    self.lines.extend( lines[ i: ] )
                    break
            else:
                return

        lines = self.lines
        for i in range( max( 1, n ), len( lines ) ):
            line = lines[i]
            if (line[:1] != ' ') and (line.find( ':' ) >= 0):
                self.paste_traceback( '\n'.join( lines[ 1: i + 1 ] ) )
                self.lines = []
                rest       = '\n'.join( lines[ i + 1: ] )
                if rest != '':
                    self.write( rest )
                break

    #---------------------------------------------------------------------------
    #  Handles 'flush' calls to stderr:
    #---------------------------------------------------------------------------

    def flush ( self ):
        """ Handles 'flush' calls to stderr.
        """
        self.stderr.flush()

    #---------------------------------------------------------------------------
    #  Handles the 'paste_traceback' event being fired:
    #---------------------------------------------------------------------------

    def paste_traceback ( self, buffer = None ):
        """ Handles the 'paste_traceback' event being fired.
        """
        if buffer is None:
            buffer = clipboard.text_data

        lines = buffer.replace( '\r\n', '\n' ).replace( '\r', '\n' ).split('\n')
        hits  = [ i for i, line in enumerate( lines )
                    if file_begin_pat.match( line ) is not None ]

        n     = len( lines )
        if (n > 0) and (lines[-1][0:1] != ' '):
            hits.append( n - 1 )

        for i in range( len( hits ) - 1 ):
            h1, h2 = hits[ i: i + 2 ]
            for j in range( h1 + 1, h2 - 1 ):
                lines[ h1 ] += lines[ j ]
                lines[ j ]   = ''

        lines = [ line for line in lines if line != '' ]

        got_match = False
        i         = 0
        n         = len( lines )
        entries   = []
        exception = 'Unknown Exception'
        while i < n:
            match = file_pat.match( lines[i] )
            if match is not None:
                got_match = True
                entries.append( TracebackEntry(
                                    file_name = match.group( 1 ),
                                    line      = int( match.group( 2 ) ),
                                    name      = match.group( 3 ),
                                    source    = lines[ i + 1 ].strip() ) )
                i += 2
            elif got_match:
                exception = lines[ i ].strip()
                break
            else:
                i += 1

        self.exception = exception
        self.traceback = entries

    #---------------------------------------------------------------------------
    #  Handles the 'buffer' trait being changed:
    #---------------------------------------------------------------------------

    def _buffer_changed ( self, buffer ):
        """ Handles the 'buffer' trait being changed.
        """
        self.paste_traceback( buffer )

    #---------------------------------------------------------------------------
    #  Handles a new traceback entry being selected:
    #---------------------------------------------------------------------------

    def _selected_changed ( self, entry ):
        """ Handles a new traceback entry being selected.
        """
        self.file_position = FilePosition( file_name = entry.file_name,
                                           line      = entry.line )

#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = TracebackViewer()

