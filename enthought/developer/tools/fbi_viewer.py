#-------------------------------------------------------------------------------
#
#  FBI Viewer plugin
#
#  Written by: David C. Morrill
#
#  Date: 07/22/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasPrivateTraits, Any, Int, Str, Code, List, Range, Enum, Button, \
           Instance, Bool

from enthought.traits.ui.api \
    import View, VGroup, HGroup, Item, ListEditor, CodeEditor, Theme

from enthought.pyface.timer.api \
    import do_later

from enthought.developer.features.api \
    import DropFile

from enthought.developer.api \
    import FilePosition, read_file

from enthought.developer.helper.fbi \
    import fbi_object

from enthought.developer.helper.themes \
    import TTitle, TButton

from enthought.developer.helper.bdb \
    import BPType

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# Editor selection color:
SelectionColor = 0xFBD391

#-------------------------------------------------------------------------------
#  'FBIViewer' plugin:
#-------------------------------------------------------------------------------

class FBIViewer ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'FBI Viewer' )
    
    # The persistence id for this object:
    id = Str( 'enthought.developer.tools.fbi_viewer.state',
              save_state_id = True )

    # Maximum number of open viewers allowed:
    max_viewers = Range( 1, 50, 50, mode = 'spinner', save_state = True )

    # The current item being inspected:
    file_position = Instance( FilePosition,
                     drop_file  = DropFile(
                     extensions = [ '.py' ],
                     tooltip    = 'Drop a Python file or file position here.' ),
                     connect    = 'to:file position' )

    # Current list of source files being viewed:
    viewers = List

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( 'viewers@',
              show_label = False,
              editor     = ListEditor( use_notebook = True,
                                       deletable    = True,
                                       page_name    = '.name',
                                       export       = 'DockWindowShell',
                                       dock_style   = 'tab' )
        )
    )

    options = View(
        Item( 'max_viewers',
              label = 'Maximum number of open viewers',
              width = -50
        ),
        title   = 'FBI Viewer Options',
        id      = 'enthought.developer.tools.fbi_viewer.options',
        buttons = [ 'OK', 'Cancel' ]
    )

    #---------------------------------------------------------------------------
    #  Handles the 'max_viewers' trait being changed:
    #---------------------------------------------------------------------------

    def _max_viewers_changed ( self, max_viewers ):
        """ Handles the 'max_viewers' trait being changed.
        """
        delta = len( self.viewers ) - max_viewers
        if delta > 0:
            del self.viewers[ : delta ]

    #---------------------------------------------------------------------------
    #  Handles the 'file_position' trait being changed:
    #---------------------------------------------------------------------------

    def _file_position_changed ( self, file_position ):
        """ Handles the 'file_position' trait being changed.
        """
        if file_position is not None:
            # Reset the current file position to None, so we are ready for a
            # new one:
            do_later( self.set, file_position = None )

            viewers = self.viewers
            for i, viewer in enumerate( viewers ):
                if ((file_position.name      == viewer.name)      and
                    (file_position.file_name == viewer.file_name) and
                    (file_position.lines     == viewer.lines)     and
                    (file_position.object    == viewer.object)):
                    viewer.selected_line = file_position.line
                    if i == (len( viewers ) - 1):
                        return
                    del viewers[i]
                    break
            else:
                # Create the viewer:
                viewer = AnFBIViewer(
                             **file_position.get( 'name', 'file_name', 'line',
                                                  'lines', 'object' ) )

                # Make sure the # of viewers doesn't exceed the maximum allowed:
                if len( viewers ) >= self.max_viewers:
                    del viewers[0]

            # Add the new viewer to the list of viewers (which will cause it to
            # appear as a new notebook page):
            viewers.append( viewer )

#-------------------------------------------------------------------------------
#  'AnFBIViewer' class:
#-------------------------------------------------------------------------------

class AnFBIViewer ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The viewer page name:
    name = Str

    # The name of the file being viewed:
    file_name = Str( draggable = 'Drag the file name.' )

    # The starting line number:
    line = Int

    # The number of lines (start at 'line'):
    lines = Int( -1 )

    # The number of lines of text in the view:
    nlines = Int

    # The object associated with this view:
    object = Any

    # The title of this view:
    title = Str

    # Should the break point trigger only for the specified object:
    object_only = Bool( False )

    # Type of breakpoint to set:
    bp_type = BPType

    # The condition the break point should trigger on:
    condition = Str

    # The currently selected line:
    selected_line = Int

    # The current cursor position:
    cursor = Int( -1 )

    # The list of lines with break points:
    bp_lines = List( Int )

    # The logical starting line (used to adjust lines passed to the FBI):
    starting_line = Int

    # Fired when a breakpoint is to be set:
    bp_set = Button( 'Set' )

    # Fired when a breakpoint is to be reset:
    bp_reset = Button( 'Reset' )

    # Does the current line have any breakpoints set on it:
    has_bp = Bool( False )

    # The source code being viewed:
    source = Code

    # The FBI module this file corresponds to:
    module = Any

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View(
        VGroup(
            TTitle( 'title' ), 
            HGroup(
                Item( 'object_only',
                      label        = 'For this object only',
                      enabled_when = 'object.object is not None'
                ),
                Item(  'bp_type',   label = 'Type' ),
                Item( 'condition', width = 200 ),
                TButton( 'bp_set',
                         label        = 'Set',
                         enabled_when = "(bp_type != 'Trace') or "
                                        "(condition.strip() != '')"
                ),
                TButton( 'bp_reset',
                         label        = 'Reset',
                         enabled_when = 'has_bp'
                ),
                show_border = True,
                label       = 'Breakpoint Modifiers'
            ),
            Item( 'source',
                  editor = CodeEditor( selected_line = 'selected_line',
                                       line          = 'cursor',
                                       mark_lines    = 'bp_lines',
                                       mark_color    = SelectionColor,
                                       auto_scroll   = False )
            ),
            show_labels = False
        )
    )

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, **traits ):
        """ Initializes the object.
        """
        super( AnFBIViewer, self ).__init__( **traits )

        source = read_file( self.file_name )
        if source is not None:
            text   = source.split( '\n' )
            nlines = self.lines
            if nlines >= 0:
                self.nlines = nlines
                line        = self.line - 1
                source      = '\n'.join( text[ line: line + nlines ] )
                self.line   = 1
                self.starting_line = line
            else:
                self.nlines = len( text )

            self.selected_line = self.cursor = self.line
            self.source        = source

            self.module = fbi_object.get_module( self.file_name )
            self.module.on_trait_change( self.update_viewer, 'bp_lines' )
            self.module.on_trait_change( self.update_viewer, 'bp_lines_items' )

            title  = self.file_name
            object = self.object
            if object is not None:
                title += '     Object: %s(0x%08X)' % (
                         object.__class__.__name__, id( object ) )
            self.title = title

            self.update_viewer()

    #---------------------------------------------------------------------------
    #  Updates the viewer when the current set of breakpoint lines changes:
    #---------------------------------------------------------------------------

    def update_viewer ( self ):
        """ Updates the viewer when the current set of breakpoint lines changes.
        """
        n        = self.nlines
        sline    = self.starting_line
        bp_lines = [ i - sline
                     for i in fbi_object.break_point_lines( self.file_name ) ]
        self.bp_lines = [ i for i in bp_lines if 0 <= i <= n ]
        self._cursor_changed()

    #---------------------------------------------------------------------------
    #  Handles the user selecting a new line:
    #---------------------------------------------------------------------------

    def _cursor_changed ( self ):
        """ Handles the user selecting a new line.
        """
        self.has_bp = (self.cursor in self.bp_lines)
        self.selected_line = self.cursor

    #---------------------------------------------------------------------------
    #  Handles the 'Set' breakpoint button being clicked:
    #---------------------------------------------------------------------------

    def _bp_set_changed ( self ):
        """ Handles the 'Set' breakpoint button being clicked.
        """
        condition = self.condition.strip()
        if self.object_only:
            self_check = ('id(self) == %d' % id( self.object ))
            if condition != '':
                condition = '(%s) and (%s)' % ( condition, self_check )
            else:
                condition = self_check

        fbi_object.add_break_point(
                 self.file_name, self.cursor + self.starting_line, self.bp_type,
                 condition )

    #---------------------------------------------------------------------------
    #  Handles the 'Reset' breakpoint button being clicked:
    #---------------------------------------------------------------------------

    def _bp_reset_changed ( self ):
        """ Handles the 'Reset' breakpoint button being clicked.
        """
        fbi_object.remove_break_point( self.file_name,
                                       self.cursor + self.starting_line )

#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = FBIViewer()

