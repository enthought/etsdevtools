#-------------------------------------------------------------------------------
#
#  FBI: Frame Based Inspector - A Traits-based debugging tool for interactively
#  inspecting the contents of the Python stack within a GUI application. The
#  tool can be invoked either after an exception occurs or at any point in the
#  normal execution of a program.
#
#  It runs as a 'modal' dialog and thus blocks further program execution until
#  the inspector exits.
#
#  Written by: David C. Morrill
#
#  Date: 01/04/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import sys

from inspect \
    import stack, getinnerframes

from os \
    import environ

from os.path \
    import split, join, isdir, abspath, normcase

from enthought.traits.api \
    import HasTraits, HasPrivateTraits, Str, Int, Instance, List, Dict, Any, \
           Code, Constant, Property, PythonValue, Button, Event, Bool, \
           TraitError, push_exception_handler

from enthought.traits.ui.api \
    import View, VSplit, VGroup, HSplit, HGroup, HFlow, Tabbed, Item, \
           TableEditor, ValueEditor, CodeEditor, InstanceEditor, TextEditor, \
           EnumEditor, ShellEditor, Handler, UI

from enthought.traits.ui.value_tree \
    import ValueTree
    
from enthought.traits.ui.wx.extra.tabular_editor \
    import TabularEditor, TabularAdapter

from enthought.traits.ui.menu \
    import NoButtons

from enthought.traits.ui.table_column \
    import ObjectColumn

from enthought.pyface.timer.api \
    import do_later

from enthought.pyface.image_resource \
    import ImageResource

from enthought.developer.helper.bdb \
    import Bdb, BPType, Breakpoint

from enthought.developer.tools.class_browser \
    import ClassBrowser, ClassBrowserPaths, CBPath

from enthought.developer.tools.object_source \
    import ObjectSource

from enthought.developer.tools.favorites_browser \
    import FavoritesBrowser

from enthought.developer.tools.universal_inspector \
    import UniversalInspector

from enthought.developer.tools.listener \
    import Listener

from enthought.developer.helper.file_position \
    import FilePosition

from enthought.developer.helper.pickle \
    import get_pickle, set_pickle

from enthought.developer.helper.themes \
    import TButton

from enthought.pyface.dock.features.api \
    import CustomFeature

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# Separator line:
separator = ('_' * 79) + '\n'

# Standard sequence types:
SequenceTypes = ( list, tuple )

# Table editor selection color:
SelectionColor = 0xFBD391

#-------------------------------------------------------------------------------
#  Global values:
#-------------------------------------------------------------------------------

# Should the next break point hit be skipped?
skip_bp = False

#-------------------------------------------------------------------------------
#  Creates the class browser object:
#-------------------------------------------------------------------------------

paths = environ.get( 'PYTHONPATH' )
if paths is None:
    paths = sys.path[:]
else:
    paths = paths.split( ';' )
paths = [ path for path in paths if isdir( path ) ]
paths.sort()
TheClassBrowser = ClassBrowser( root = ClassBrowserPaths(
                         paths = [ CBPath( path = path ) for path in paths ] ) )
TheObjectSource     = ObjectSource()
TheListener         = Listener()
TheFavoritesBrowser = FavoritesBrowser(
    id = 'enthought.developer.helper.fbi.favorites_browser.state'
)
TheInspector = UniversalInspector(
    id = 'enthought.developer.helper.fbi.universal_inspector.state'
)

#-------------------------------------------------------------------------------
#  Returns the canonic form of a specified file name:
#-------------------------------------------------------------------------------

def canonic ( file_name ):
    return normcase( abspath( file_name ) )

#-------------------------------------------------------------------------------
#  Evaluates an expression in the context of the current debugger stack frame:
#-------------------------------------------------------------------------------

def eval_in_frame ( value ):
    """ Evaluates an expression in the context of the current debugger stack
        frame.
    """
    global fbi_object

    try:
        if isinstance( eval( value, globals(), fbi_object.frame.variable ),
                           HasTraits ):
            return value
    except:
        pass

    return 0

#-------------------------------------------------------------------------------
#  Returns the contents of a text file:
#-------------------------------------------------------------------------------

def text_file ( file_name ):
    """ Returns the contents of a text file.
    """
    fh = None
    try:
        fh     = open( file_name, 'rb' )
        result = fh.read()
    except:
        result = ''
    if fh is not None:
        fh.close()
    return result

#-------------------------------------------------------------------------------
#  'FBIValue' class:
#-------------------------------------------------------------------------------

class FBIValue ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Name of the python value:
    name = Str

    # Type of python value:
    type = Str

    # The actual value:
    value = Any

    # String represention of the value:
    str_value = Str

#-------------------------------------------------------------------------------
#  'DataWatch' class:
#-------------------------------------------------------------------------------

class DataWatch ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Expression used to evaluate and define 'object':
    expression = Str

    # Object being watched:
    object = Instance( HasTraits )

    # Trait being watched ('Any' == 'all traits'):
    trait = Str( 'Any' )

    # List of traits that can be watched:
    traits = List( Str, [ 'Any' ] )

    # Optional condition that must be true before watch triggers:
    condition = Str

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View( Item( 'expression{Object}',
                       editor = TextEditor( evaluate = eval_in_frame ) ),
                 Item( 'trait', editor = EnumEditor( name = 'traits' ) ),
                 Item( 'condition' ),
                 title   = 'Create Data Watch',
                 kind    = 'livemodal',
                 buttons = [ 'OK', 'Cancel' ] )

    #---------------------------------------------------------------------------
    #  Handles the 'expression' trait being changed:
    #---------------------------------------------------------------------------

    def _expression_changed ( self, expr ):
        """ Handles the 'expression' trait being changed.
        """
        global fbi_object

        try:
            self.object = eval( expr, globals(), fbi_object.frame.variable )
        except:
            pass

    #---------------------------------------------------------------------------
    #  Handles the 'object' trait being changed:
    #---------------------------------------------------------------------------

    def _object_changed ( self, object ):
        """ Handles the 'object' trait being changed.
        """
        names = object.trait_names()
        names.sort()
        self.traits = ([ 'Any' ] + names)

#-------------------------------------------------------------------------------
#  'FBIModule' class:
#-------------------------------------------------------------------------------

class FBIModule ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # File defining the module:
    file_name = Str

    # List of the line numbers of the active break points in the module:
    bp_lines = List( Int )

#-------------------------------------------------------------------------------
#  FBIValue table editor definition:
#-------------------------------------------------------------------------------

#fbi_value_editor = TableEditor(
#    columns   = [ ObjectColumn( name     = 'name',
#                                editable = False ),
#                  ObjectColumn( name     = 'type',
#                                editable = False,
#                                horizontal_alignment = 'center' ),
#                  ObjectColumn( name     = 'str_value',
#                                label    = 'Value',
#                                editable = False ),
#                ],
#    selection_bg_color = SelectionColor,
#    selection_color    = 'black',
#    editable           = False,
#    auto_size          = False,
#    sortable           = False,
#    configurable       = False
#)

class FBIValueAdapter ( TabularAdapter ):
    
    columns = [ ( 'Name',  'name' ),
                ( 'Type',  'type' ),
                ( 'Value', 'str_value' ) ]
                
    type_alignment = Constant( 'center' )
    
fbi_value_editor = TabularEditor(
    editable   = False,
    adapter    = FBIValueAdapter(),
    operations = []
)

#-------------------------------------------------------------------------------
#  'StackFrame' class:
#-------------------------------------------------------------------------------

class StackFrame ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # File name:
    file_name = Str

    # File path:
    file_path = Str

    # Function name:
    function_name = Str

    # Line number:
    line = Int

    # Source code line being executed:
    source = Str

    # Module source code:
    module_source = Code

    # List of local variables (including the arguments):
    local_variables = List( FBIValue )

    # Frame local values:
    frame_locals = PythonValue

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, stack_frame ):
        """ Initializes the object.
        """
        frame, file_name, line, self.function_name, lines, index = stack_frame
        self.file_path, self.file_name = split( file_name )

        # Create the list of local variables:
        locals  = self.frame_locals = frame.f_locals
        nlocals = frame.f_code.co_nlocals
        args    = frame.f_code.co_argcount
        names   = frame.f_code.co_varnames
        if (args < nlocals) and (names[0] == 'self'):
            args += 1
        variables = []
        for i in range( nlocals ):
            try:
                # The following statement could fail if the local has not been
                # initialized yet:
                name  = names[i]
                value = locals[ name ]
                type  = 'local'
                if i < args:
                    type = 'argument'
                variables.append( FBIValue( name      = name,
                                            type      = type,
                                            value     = value,
                                            str_value = repr( value ) ) )
            except:
                pass
        self.local_variables = variables

        # Read the module source code:
        self.module_source = text_file( file_name )

        # Get the source code line being executed:
        try:
            self.source = lines[ index ].strip()
        except:
            self.source = '???'

        # Set the current source code line number being executed:
        self.line = line

#-------------------------------------------------------------------------------
#  StackFrame table editor definition:
#-------------------------------------------------------------------------------

#stack_frame_editor = TableEditor(
#    columns   = [ ObjectColumn( name     = 'function_name',
#                                label    = 'Function',
#                                editable = False ),
#                  ObjectColumn( name     = 'file_name',
#                                label    = 'File Name',
#                                editable = False ),
#                  ObjectColumn( name     = 'file_path',
#                                label    = 'File Path',
#                                editable = False ),
#                  ObjectColumn( name     = 'line',
#                                editable = False,
#                                horizontal_alignment = 'center' ),
#                  ObjectColumn( name     = 'source',
#                                editable = False ),
#                ],
#
#    selection_bg_color = SelectionColor,
#    selection_color    = 'black',
#    configurable       = False,
#    editable           = False,
#    auto_size          = False,
#    sortable           = False,
#    selected           = 'frame'
#)

class StackFrameAdapter ( TabularAdapter ):
    
    columns = [ ( 'Function',  'function_name' ),
                ( 'File Name', 'file_name' ),
                ( 'File Path', 'file_path' ),
                ( 'Line',      'line' ),
                ( 'Source',    'source' ) ]
                
    line_alignment = Constant( 'center' )
    
stack_frame_editor = TabularEditor(
    selected   = 'frame',
    editable   = False,
    adapter    = StackFrameAdapter(),
    operations = []
)

#-------------------------------------------------------------------------------
#  Break points table editor definition:
#-------------------------------------------------------------------------------

bp_table_editor = TableEditor(
    columns   = [ ObjectColumn( name     = 'module',
                                editable = False ),
                  ObjectColumn( name     = 'line',
                                editable = False,
                                horizontal_alignment = 'center' ),
                  ObjectColumn( name     = 'bp_type',
                                label    = 'BP Type',
                                editable = True,
                                horizontal_alignment = 'center' ),
                  ObjectColumn( name     = 'code',
                                label    = 'Condition',
                                editable = True ),
                  ObjectColumn( name     = 'enabled',
                                horizontal_alignment = 'center' ),
                  ObjectColumn( name     = 'hits',
                                editable = False,
                                horizontal_alignment = 'center' ),
                  ObjectColumn( name     = 'count',
                                editable = False,
                                horizontal_alignment = 'center' ),
                  ObjectColumn( name     = 'ignore',
                                editable = True,
                                horizontal_alignment = 'center' ),
                  ObjectColumn( name     = 'source',
                                editable = False ),
                ],
    other_columns = [ ObjectColumn( name     = 'file',
                                    editable = False ),
                      ObjectColumn( name     = 'path',
                                    editable = False ),
                      ObjectColumn( name     = 'end_line',
                                    editable = False )
                    ],
    selection_bg_color = SelectionColor,
    selection_color    = 'black',
    deletable          = True,
    configurable       = True,
    editable           = True,
    auto_size          = False,
    sortable           = True,
    selected           = 'selected'
)

#-------------------------------------------------------------------------------
#  'Breakpoints' class:
#-------------------------------------------------------------------------------

class Breakpoints ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The list of currently defined break points:
    break_points = List( Instance( Breakpoint ) )

    # The currently selected break points:
    selected = Instance( Breakpoint )

    # Fired when user wants to restore all saved break points:
    restore_bp = Instance( CustomFeature, {
                            'image':   ImageResource( 'fbi_restore_bp' ),
                            'click':   'restore',
                            'tooltip': 'Click to restore all saved break '
                                       'points.'
                         },
                         custom_feature = True )

    # Clear all current break points:
    clear_bp = Instance( CustomFeature, {
                            'image':   ImageResource( 'fbi_clear_bp' ),
                            'enabled': False,
                            'click':   'clear',
                            'tooltip': 'Click to clear all break points.'
                         },
                         custom_feature = True )

    # Have break points been restored yet?
    restored = Bool( False )

    # Fired when a break point has been modified:
    modified = Event

    # The file position of the currently selected break point:
    file_position = Instance( FilePosition,
                    connect   = 'from:file position',
                    draggable = "Drag the current break point's file position" )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( 'break_points',
              show_label = False,
              label      = 'Break Points',
              id         = 'break_points',
              editor     = bp_table_editor
        ),
        id = 'enthought.developer.helper.fbi.break_points'
    )

    #---------------------------------------------------------------------------
    #  Handles the user requesting that all break points be cleared:
    #---------------------------------------------------------------------------

    def clear ( self ):
        """ Handles the user requesting that all break points be cleared.
        """
        del self.break_points[:]

    #---------------------------------------------------------------------------
    #  Restores all previously saved break points:
    #---------------------------------------------------------------------------

    def restore ( self ):
        """ Restores all previously saved break points.
        """
        if not self.restored:
            self.restored           = True
            self.restore_bp.enabled = False
            bps = [ bp for bp in get_pickle(
                       'enthought.developer.helper.fbi.break_points.state', [] )
                       if bp.restore() ]
            self._no_save = True
            self.break_points.extend( bps )
            self._no_save = False

            for bp in bps:
                fbi_bdb.restore_break( bp )
                fbi_object.mark_bp_at( bp )

            fbi_bdb.begin_trace()

    #---------------------------------------------------------------------------
    #  Persists all of the current break points:
    #---------------------------------------------------------------------------

    def save ( self ):
        """ Persists all of the current break points.
        """
        # Merge in any previously saved break points (if necessary):
        self.restore()

        # Now save out all current break points:
        set_pickle( 'enthought.developer.helper.fbi.break_points.state',
                    self.break_points[:] )

    #---------------------------------------------------------------------------
    #  Adds a list of break points:
    #---------------------------------------------------------------------------

    def add ( self, *bps ):
        """ Adds a list of break points.
        """
        self.break_points.extend( bps )

    #---------------------------------------------------------------------------
    #  Removes a list of break points:
    #---------------------------------------------------------------------------

    def remove ( self, *bps ):
        """ Removes a list of break points.
        """
        break_points = self.break_points[:]
        for bp in bps:
            break_points.remove( bp )
        self.break_points = break_points

    #---------------------------------------------------------------------------
    #  Removes any temporary break points for the specified frame:
    #---------------------------------------------------------------------------

    def remove_temporaries_for ( self, frame ):
        """ Removes any temporary break points for the specified frame.
        """
        bps    = self.get_break_points_for( frame, frame.line )
        delete = [ i for i, bp in bps if bp.bp_type == 'Temporary' ]
        if len( delete ) > 0:
            delete.sort( lambda l, r: cmp( r, l ) )
            for i in delete:
                del self.break_points[i]

    #---------------------------------------------------------------------------
    #  Returns the break points (if any) at a specified frame line:
    #---------------------------------------------------------------------------

    def get_break_points_for ( self, frame, line ):
        """ Returns the break point (if any) at a specified frame line.
        """
        file   = canonic( join( frame.file_path, frame.file_name ) )
        result = []
        for i, bp in enumerate( self.break_points ):
            if (file == bp.file) and (line == bp.line):
                result.append( ( i, bp ) )

        return result

    #---------------------------------------------------------------------------
    #  Check the status of any features:
    #---------------------------------------------------------------------------

    def check_bps ( self ):
        """ Check the status of any features.
        """
        self.clear_bp.enabled = (len( self.break_points ) > 0)
        do_later( self.save )

    #---------------------------------------------------------------------------
    #  Handles the 'break_points' trait being changed:
    #---------------------------------------------------------------------------

    def _break_points_changed ( self, bps ):
        """ Handles the 'break_points' trait being changed.
        """
        for bp in bps:
            bp.owner = self

        self.check_bps()

    def _break_points_items_changed ( self, event ):
        """ Handles the 'break_points' trait being changed.
        """
        for bp in event.added:
            bp.owner = self

        for bp in event.removed:
            fbi_bdb.clear_bp( bp )
            if len( fbi_bdb.get_breaks( bp.file, bp.line ) ) == 0:
                fbi_object.get_module( bp.file ).bp_lines.remove( bp.line )

        self.check_bps()

    #---------------------------------------------------------------------------
    #  Handles the 'modified' trait being changed:
    #---------------------------------------------------------------------------

    def _modified_changed ( self ):
        """ Handles the 'modified' trait being changed.
        """
        self.check_bps()

    #---------------------------------------------------------------------------
    #  Handles the 'selected' trait being changed:
    #---------------------------------------------------------------------------

    def _selected_changed ( self, selected ):
        """ Handles the 'selected' trait being changed.
        """
        if selected is not None:
            self.file_position = FilePosition( file_name = selected.file,
                                               line      = selected.line )

# Create the exported object:
break_points = Breakpoints()

#-------------------------------------------------------------------------------
#  Data watches table editor definition:
#-------------------------------------------------------------------------------

dw_table_editor = TableEditor(
    columns = [ ObjectColumn( name     = 'object',
                              editable = False ),
                ObjectColumn( name     = 'trait',
                              editable = False,
                              horizontal_alignment = 'center' ),
                ObjectColumn( name     = 'condition',
                              editable = False )
              ],
    selection_bg_color = SelectionColor,
    selection_color    = 'black',
    configurable       = True,
    deletable          = True,
    auto_size          = False,
    sortable           = True,
    row_factory        = DataWatch,
    row_factory_kw     = { 'expression': 'self' }
)

#class DWTableAdapter ( TabularAdapter ):
#    
#    columns = [ ( 'Object',    'object' ),
#                ( 'Trait',     'trait' ),
#                ( 'Condition', 'condition' ) ]
#                
#    trait_alignment = Constant( 'center' )
#    
#dw_table_editor = TabularEditor(
#    editable   = False,
#    adapter    = DWTableAdapter(),
#    operations = []
#)

#-------------------------------------------------------------------------------
#  'FBIBdb' class:
#-------------------------------------------------------------------------------

class FBIBdb ( Bdb ):

    def __init__ ( self ):
        Bdb.__init__( self )
        self.bp = {}

    def user_call ( self, frame, argument_list ):
        """ This method is called when there is the remote possibility
            that we ever need to stop in this function.
        """
        if self.break_here(frame):
            fbi( msg = 'Break point', offset = 3, debug_frame = frame )

    def user_line ( self, frame ):
        """ This method is called when we stop or break at this line.
        """
        global skip_bp
        
        if skip_bp:
            skip_bp = False
        else:
            fbi( msg = 'Step', offset = 3, debug_frame = frame, 
                 allow_exception = False )

    def user_return ( self, frame, return_value ):
        """ This method is called when a return trap is set here.
        """
        fbi( msg = 'Return', offset = 3, debug_frame = frame, 
             allow_exception = False )

    def user_exception ( self, frame, ( exc_type, exc_value, exc_traceback ) ):
        """ This method is called if an exception occurs, but only if we are
            to stop at or just below this level.
        """
        fbi( offset = 3, debug_frame = frame )

    def set_trace ( self ):
        """Start debugging from here."""
        frame = sys._getframe().f_back
        code  = frame.f_code
        key   = ( code.co_filename, frame.f_lineno )
        if key in self.bp:
            return
        self.bp[ key ] = None
        frame = frame.f_back
        self.reset()
        while frame:
            frame.f_trace = self.trace_dispatch
            self.botframe = frame
            frame         = frame.f_back
        self.set_step()
        sys.settrace( self.trace_dispatch )

    def begin_trace ( self ):
        """Start debugging from here."""
        sys.settrace( None )
        frame = sys._getframe().f_back
        code  = frame.f_code
        frame = frame.f_back
        self.reset()
        while frame:
            frame.f_trace = self.trace_dispatch
            self.botframe = frame
            frame         = frame.f_back
        self.set_continue()
        sys.settrace( self.trace_dispatch )

# Create the global debugger instance:
fbi_bdb = FBIBdb()

# Insert a call to this function into your program to invoke the debugger:
def bp ( condition = True ):
    if condition:
        fbi_bdb.set_trace()

# Insert a call to this function into your program to invoke the debugger if
# the FBI is enabled:
def if_bp ( condition = True ):
    global fbi_enabled

    if fbi_enabled and condition:
        fbi_bdb.set_trace()

    return fbi_enabled

#-------------------------------------------------------------------------------
#  'FBI' class:
#-------------------------------------------------------------------------------

class FBI ( Handler ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Message to display to the user:
    msg = Str

    # The list of stack frames currently being inspected:
    frames = List( StackFrame )

    # Current frame being inspected:
    frame = Instance( StackFrame, allow_none = True )

    # A scratch pad area for accumulating interesting values to look at:
    value_tree = ValueTree

    # The currently defined break points:
    break_points = Constant( break_points )

    # List of currently active data watches:
    data_watches = List( Instance( DataWatch ) )

    # The set of modules containing break point information:
    modules = Dict( Str, Instance( FBIModule ) )

    # A class browser:
    class_browser = Constant( TheClassBrowser )

    # An object source:
    object_source = Constant( TheObjectSource )

    # A favorites browser:
    favorites_browser = Constant( TheFavoritesBrowser )

    # A universal inspector:
    inspector = Constant( TheInspector )

    # A listener:
    listener = Constant( TheListener )

    # A wiretap:
    wiretap = Property

    # An FBI Viewer
    fbi_viewer = Property

    # List of local variables (including the arguments) for the current frame:
    local_variables = List( FBIValue )

    # Current selected frame's locals:
    frame_locals = PythonValue

    # Ignore the next request to set a break point?
    ignore_bp = Bool( False )

    # Is the FBI being run under an app that has a UI:
    has_ui = Bool( True )
    
    # Is the FBI being run modally:
    is_modal = Bool( True )

    # The traits UI associated with this object:
    ui = Instance( UI )

    # The debugger 'Step' button:
    step = Button( 'Step', image       = ImageResource( 'fbi_step' ),
                           orientation = 'horizontal' )

    # The debugger 'Next' button:
    next = Button( 'Next', image       = ImageResource( 'fbi_next' ),
                           orientation = 'horizontal' )

    # The debugger 'Return' button:
    ret = Button( 'Return', image       = ImageResource( 'fbi_return' ),
                            orientation = 'horizontal' )

    # The debugger 'Go' button:
    go = Button( 'Go', image       = ImageResource( 'fbi_go' ),
                       orientation = 'horizontal' )

    # The debugger 'Quit' button:
    quit = Button( 'Quit', image       = ImageResource( 'fbi_quit' ),
                           orientation = 'horizontal' )

    # Frame information received from the debugger:
    debug_frame = Any

    #---------------------------------------------------------------------------
    #  Trait view definitions:
    #---------------------------------------------------------------------------

    view = View(
               VSplit(
                   HFlow(
                       TButton( 'step', 
                                label        = 'Step',
                                image        = 'fbi_step',
                                width        = 80,
                                enabled_when = 'debug_frame is not None' ),
                       TButton( 'next', 
                                label        = 'Next',
                                image        = 'fbi_next',
                                width        = 80,
                                enabled_when = 'debug_frame is not None' ),
                       TButton( 'ret', 
                                label        = 'Return',
                                image        = 'fbi_return',
                                width        = 80,
                                enabled_when = 'debug_frame is not None' ),
                       TButton( 'go', 
                                label        = 'Go',
                                image        = 'fbi_go',
                                width        = 80,
                                enabled_when = 'debug_frame is not None' ),
                       TButton( 'quit', 
                                label        = 'Quit',
                                image        = 'fbi_quit',
                                width        = 80,
                                enabled_when = 'debug_frame is not None' ),
                       dock        = 'vertical',
                       label       = 'Toolbar',
                       show_labels = False
                   ),
                   VGroup( 'msg~',
                           dock        = 'vertical',
                           label       = 'Status',
                           show_labels = False
                   ),
                   Tabbed(
                       Item( 'frames',
                             show_label = False,
                             label      = 'Stack Frames',
                             id         = 'frames',
                             editor     = stack_frame_editor
                       ),
                       Item( 'break_points@',
                             show_label = False,
                             label      = 'Break Points',
                             export     = 'DockShellwindow',
                             editor     = InstanceEditor( id = 'internal' )
                       ),
                       Item( 'data_watches',
                             show_label = False,
                             label      = 'Data Watches',
                             id         = 'data_watches',
                             editor     = dw_table_editor
                       ),
                       Item( 'value_tree',
                             show_label = False,
                             label      = 'Watch Values',
                             export     = 'DockShellwindow'
                       ),
                       Item( 'class_browser@',
                             show_label = False,
                             label      = 'Class Browser',
                             export     = 'DockShellWindow'
                       ),
                       Item( 'object_source@',
                             show_label = False,
                             label      = 'Object Source',
                             export     = 'DockShellWindow'
                       ),
                       Item( 'favorites_browser@',
                             show_label = False,
                             label      = 'Favorites Browser',
                             export     = 'DockShellWindow'
                       ),
                       Item( 'inspector@',
                             show_label = False,
                             label      = 'Universal Inspector',
                             export     = 'DockShellWindow'
                       ),
                       Item( 'wiretap@',
                             show_label = False,
                             label      = 'Wire Tap',
                             editor     = InstanceEditor(),
                             export     = 'DockShellWindow'
                       ),
                       Item( 'listener@',
                             show_label = False,
                             label      = 'Listener',
                             export     = 'DockShellWindow'
                       ),
                       Item( 'fbi_viewer@',
                             show_label = False,
                             label      = 'Source View',
                             editor     = InstanceEditor(),
                             export     = 'DockShellWindow'
                       ),
                       show_labels = False
                   ),
                   VSplit(
                       Item( 'local_variables',
                             show_label = False,
                             label      = 'Local Variables',
                             id         = 'local_variables',
                             editor     = fbi_value_editor,
                             export     = 'DockShellWindow'
                       ),
                       Tabbed(
                           Item( 'frame_locals',
                                 show_label = False,
                                 label      = 'Variable Values',
                                 editor     = ValueEditor(),
                                 export     = 'DockShellWindow'
                           ),
                           Item( 'frame_locals',
                                 id         = 'python_shell',
                                 show_label = False,
                                 label      = 'Python Shell',
                                 editor     = ShellEditor( share = True ),
                                 export     = 'DockShellWindow'
                           )
                       )
                   ),
                   id          = 'splitter',
                   show_labels = False
               ),
               title     = 'FBI: Frame Based Inspector',
               id        = 'enthought.developer.helper.fbi',
               kind      = 'livemodal',
               dock      = 'tab',
               width     = 0.8,
               height    = 0.8,
               resizable = True,
               buttons   = NoButtons
           )

    #---------------------------------------------------------------------------
    #  Initializes the controls of a user interface:
    #---------------------------------------------------------------------------

    def init ( self, info ):
        """ Initializes the controls of a user interface.
        """
        self.ui = info.ui

    #---------------------------------------------------------------------------
    #  Implementation of the 'wiretap' property:
    #---------------------------------------------------------------------------

    def _get_wiretap ( self ):
        if self._wiretap is None:
           from enthought.developer.tools.wiretap import Wiretap

           self._wiretap = Wiretap()

        return self._wiretap

    #---------------------------------------------------------------------------
    #  Implementation of the 'fbi_viewer' property:
    #---------------------------------------------------------------------------

    def _get_fbi_viewer ( self ):
        if self._fbi_viewer is None:
            from enthought.developer.tools.fbi_viewer import FBIViewer

            self._fbi_viewer = FBIViewer(
                id = 'enthought.developer.helper.fbi.fbi_viewer.state'
            )

        return self._fbi_viewer

    #---------------------------------------------------------------------------
    #  Handles the 'frames' trait being changed:
    #---------------------------------------------------------------------------

    def _frames_changed ( self, frames ):
        """ Handles the 'frames' trait being changed.
        """
        if len( frames ) > 0:
            self.ignore_bp = True
            self.frame     = frame = frames[0]
            self.break_points.remove_temporaries_for( frame )

    #---------------------------------------------------------------------------
    #  Handles the 'Step' button being clicked:
    #---------------------------------------------------------------------------

    def _step_changed ( self ):
        """ Handles the 'Step' button being clicked.
        """
        fbi_bdb.set_step()
        self.exit_ui()

    #---------------------------------------------------------------------------
    #  Handles the 'Next' button being clicked:
    #---------------------------------------------------------------------------

    def _next_changed ( self ):
        """ Handles the 'Next' button being clicked.
        """
        fbi_bdb.set_next( self.debug_frame )
        self.exit_ui()

    #---------------------------------------------------------------------------
    #  Handles the 'Return' button being clicked:
    #---------------------------------------------------------------------------

    def _ret_changed ( self ):
        """ Handles the 'Return' button being clicked.
        """
        """ Handles the 'Return' button being clicked.
        """
        fbi_bdb.set_return( self.debug_frame )
        self.exit_ui()

    #---------------------------------------------------------------------------
    #  Handles the 'Go' button being clicked:
    #---------------------------------------------------------------------------

    def _go_changed ( self ):
        """ Handles the 'Go' button being clicked.
        """
        fbi_bdb.set_continue()
        self.exit_ui()

    #---------------------------------------------------------------------------
    #  Handles the 'Quit' button being clicked:
    #---------------------------------------------------------------------------

    def _quit_changed ( self ):
        """ Handles the 'Quit' button being clicked.
        """
        fbi_bdb.set_quit()
        self.debug_frame = None
        self.ui.dispose( True )

    #---------------------------------------------------------------------------
    #  Handles a DataWatch item being added or deleted:
    #---------------------------------------------------------------------------

    def _data_watches_items_changed ( self, event ):
        """ Handles a DataWatch item being added or deleted.
        """
        for dw in event.added:
            if dw.object is not None:
                trait = dw.trait
                if trait == 'Any':
                    trait = None
                fbi( monitor = ( dw.object, trait, dw.condition ) )

        for dw in event.removed:
            if dw.object is not None:
                trait = dw.trait
                if trait == 'Any':
                    trait = None
                fbi( monitor = ( dw.object, trait, dw.condition ),
                     remove  = True )

    #---------------------------------------------------------------------------
    #  Handles a request to close a dialog-based user interface by the user:
    #---------------------------------------------------------------------------

    def close ( self, info, is_ok ):
        """ Handles a request to close a dialog-based user interface by the user.
        """
        if self.debug_frame is not None:
            fbi_bdb.set_quit()
            self.debug_frame = None
        return True

    #---------------------------------------------------------------------------
    #  Exits the user interface:
    #---------------------------------------------------------------------------

    def exit_ui ( self ):
        """ Exits the user interface.
        """
        global is_modal
        
        self.debug_frame     = None
        self.frames          = []
        self.local_variables = []
        self.frame_locals    = {}
        if is_modal:
            self.ui.save_prefs()
            self.ui.control.EndModal( True )

    #---------------------------------------------------------------------------
    #  Handles the user selecting a new stack frame:
    #---------------------------------------------------------------------------

    def _frame_changed ( self, frame ):
        """ Handles the user selecting a new stack frame.
        """
        self.ignore_bp = True
        self.fbi_viewer.file_position = FilePosition(
                           name      = frame.function_name,
                           file_name = join( frame.file_path, frame.file_name ),
                           line      = frame.line )
        self.frame_locals    = frame.frame_locals
        self.local_variables = frame.local_variables

    #---------------------------------------------------------------------------
    #  Adds (or replaces) a break point:
    #---------------------------------------------------------------------------

    def add_break_point ( self, file_name, line, bp_type = 'Breakpoint', 
                                code = '', end_line = None ):
        """ Adds (or replaces) a break point.
        """
        file_name = canonic( file_name )
        bp = fbi_bdb.set_break( file_name, line, bp_type, code, end_line )
        self.break_points.add( bp )
        self.mark_bp_at( bp )

        fbi_bdb.begin_trace()

    #---------------------------------------------------------------------------
    #  Ensures we have a specified file line marked as having a break point:
    #---------------------------------------------------------------------------

    def mark_bp_at ( self, bp ):
        """ Ensures we have a specified file line marked as having a break point.
        """
        bp_lines = self.get_module( bp.file ).bp_lines
        for line in xrange( bp.line, bp.end_line ):
            if line not in bp_lines:
                bp_lines.append( line )

    #---------------------------------------------------------------------------
    #  Removes a break point on a specified file or single line within the file:
    #---------------------------------------------------------------------------

    def remove_break_point ( self, file_name, line = None, type = None ):
        """ Removes all break point on a specified file or single line within
            the file.
        """
        file_name = canonic( file_name )
        
        if line is None:
            bps = fbi_bdb.clear_all_file_breaks( file_name, type = type )
        else:
            bps = fbi_bdb.clear_break( file_name, line, type = type )
            
        if len( bps ) > 0:
            self.break_points.remove( *bps )
            lines = set()
            for bp in bps:
                lines.update( xrange( bp.line, bp.end_line ) )
                
            bp_lines = self.get_module( file_name ).bp_lines
            for line in lines:
                if not fbi_bdb.get_break( file_name, line ):
                    bp_lines.remove( line )

    #---------------------------------------------------------------------------
    #  Returns the list of lines containing break points for a specified file:
    #---------------------------------------------------------------------------

    def break_point_lines ( self, file_name ):
        """ Returns the list of lines containing breakpoints for a specified
            file.
        """
        return self.get_module( file_name ).bp_lines[:]

    #---------------------------------------------------------------------------
    #  Returns the FBIModule corresponding to a specified frame:
    #---------------------------------------------------------------------------

    def get_module_for ( self, frame ):
        """ Gets the FBIModule corresponding to a specified frame.
        """
        return self.get_module( join( frame.file_path, frame.file_name ) )

    #---------------------------------------------------------------------------
    #  Returns the FBIModule corresponding to a specified file path and name:
    #---------------------------------------------------------------------------

    def get_module ( self, file_name ):
        """ Returns the FBIModule corresponding to a specified file path and
            name.
        """
        file_name = canonic( file_name )
        module    = self.modules.get( file_name )
        if module is not None:
            return module

        self.modules[ file_name ] = module = FBIModule( file_name = file_name )
        return module

#---------------------------------------------------------------------------
#  Enables/Disables FBI to handle unhandled exceptions:
#---------------------------------------------------------------------------

# Global flag indicating whether or not the FBI is enabled:
fbi_enabled = False

# Does the application have a GUI interface?
has_gui = True

# Have DockWindow features been enabled yet?
has_features = False

# Should the FBI run modally?
is_modal = True

# Original 'sys.excepthook' handler:
saved_excepthook = None

# The FBI window:
fbi_object = FBI()
fbi_ui     = None

def enable_fbi ( enabled = True, gui = True ):
    """ Enables/Disables FBI to handle unhandled exceptions.
    """
    global fbi_enabled, has_gui, saved_excepthook

    fbi_enabled = enabled
    has_gui     = gui
    if enabled:
        sys.excepthook, saved_excepthook = fbi_exception, sys.excepthook
        try:
            push_exception_handler( handler = lambda a, b, c, d: None, 
                                    reraise_exceptions = True, 
                                    main   = True, 
                                    locked = True )
        except:
            print 'Could not set Traits notification exception handler'

def fbi_exception ( type, value, traceback, msg = '', gui = None, offset = 0,
                    debug_frame = None ):
    global fbi_object, fbi_ui, fbi_enabled, has_gui, has_features, is_modal, \
           saved_excepthook

    if gui is not None:
        has_gui = gui

    if value is None:
        if msg == '':
            msg = 'Called the FBI'
        frames = [ StackFrame( frame ) for frame in stack( 15 )[ offset + 2: ] ]
    else:
        msg    = 'Exception: %s' % str( value )
        frames = [ StackFrame( frame )
                   for frame in getinnerframes( traceback, 15 ) ]
        frames.reverse()
        frames.extend( [ StackFrame( frame ) for frame in stack( 15 )[3:] ] )

    enabled = fbi_enabled
    if enabled:
        fbi_enabled    = False
        sys.excepthook = saved_excepthook
        
    if not has_features:
        has_features = True
        try:
            from enthought.pyface.dock.features.api import add_standard_features
            add_standard_features()
        except:
            pass

    if (fbi_ui is None) or (fbi_ui.control is None):
        if has_gui:
            fbi_object.set( msg         = msg,
                            frames      = frames,
                            debug_frame = debug_frame )
            kind = 'live'
            if is_modal:
                kind = 'livemodal'
                
            fbi_ui = fbi_object.edit_traits( kind = kind )
        else:
            fbi_object.set( msg         = msg,
                            frames      = frames,
                            debug_frame = debug_frame,
                            has_ui      = False ).configure_traits()
            has_gui = False
    else:
        fbi_object.set( msg = msg, frames = frames, debug_frame = debug_frame )
        
        if is_modal:
            fbi_ui.control.ShowModal()
        else:
            fbi_ui.control.Raise()

    if enabled:
        fbi_enabled    = True
        sys.excepthook = fbi_exception

#-------------------------------------------------------------------------------
#  Calls the FBI if it has been enabled:
#-------------------------------------------------------------------------------

def if_fbi ( msg = '', stop = True, gui = None, monitor = None,
             remove = False, offset = 0, debug_frame = None ):
    """ Calls the FBI if it has been enabled.
    """
    global fbi_enabled, fbi_wiretap, has_gui

    if fbi_enabled:
        if monitor is not None:
            if gui is not None:
                has_gui = gui
            fbi_wiretap.monitor( monitor, remove )
        elif stop:
            fbi_exception( msg         = msg,
                           gui         = gui,
                           offset      = offset,
                           debug_frame = debug_frame,
                           *sys.exc_info() )

    return fbi_enabled

#-------------------------------------------------------------------------------
#  Creates and displays an FBI object:
#-------------------------------------------------------------------------------

def fbi ( msg = '', stop = True, gui = None, monitor = None, remove = False,
          offset = 0, debug_frame = None, allow_exception = True ):
    """ Creates and displays an FBI object.
    """
    global fbi_wiretap, has_gui

    if monitor is not None:
        if gui is not None:
            has_gui = gui
        fbi_wiretap.wiretap( monitor, remove )
        
    elif stop:
        if allow_exception:
            args = sys.exc_info()
        else:
            args = ( None, None, None )
            
        fbi_exception( msg         = msg,
                       gui         = gui,
                       offset      = offset,
                       debug_frame = debug_frame,
                       *args )
                       
#-------------------------------------------------------------------------------
#  Allows an application to easily set-up and use the FBI debugger:  
#-------------------------------------------------------------------------------
                                              
def use_fbi ( stop = False, restore = True, modal = True ):
    """ Allows an application to easily set-up and use the FBI debugger.
    """
    global fbi_object, skip_bp, is_modal
    
    from enthought.developer.api import file_watch
    from ex_fbi                  import SavedBreakPoints
    
    skip_bp  = (not stop)
    is_modal = modal
    
    def bp_watch ( file_name ):
        SavedBreakPoints().restore()
    
    enable_fbi()
    file_name = SavedBreakPoints().file_name 
    file_watch.watch( bp_watch, file_name )
    
    # Restore persistent break points (if requested):
    if restore:
        fbi_object.break_points.restore()
        bp_watch( file_name )

#-------------------------------------------------------------------------------
#  'FBIInvoker' class:
#-------------------------------------------------------------------------------

class FBIInvoker ( object ):

    def invoke ( cls, event ):
        fbi()

    invoke = classmethod( invoke )

#-------------------------------------------------------------------------------
#  'Wiretap' class:
#-------------------------------------------------------------------------------

class Wiretap ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Number of active 'entire object' wiretaps:
    count = Int

    # Set of 'trait level' wiretaps in effect:
    traits = Dict #( Str, Dict )

    #---------------------------------------------------------------------------
    #  Adds a new 'entire object' wiretap:
    #---------------------------------------------------------------------------

    def add_object ( self, object, condition ):
        """ Adds a new 'entire object' wiretap.
        """
        self.add_condition( '', condition )
        self.count += 1
        if self.count == 1:
            for trait in self.traits.keys():
                object.on_trait_change( self.trait_change, trait,
                                        remove = True )
            object.on_trait_change( self.trait_change )

    #---------------------------------------------------------------------------
    #  Removes an 'entire object' wiretap:
    #---------------------------------------------------------------------------

    def remove_object ( self, object, condition ):
        """ Removes an 'entire object' wiretap.
        """
        self.remove_condition( '', condition )
        self.count -= 1
        if self.count == 0:
            object.on_trait_change( self.trait_change, remove = True )
            for trait in self.traits.keys():
                object.on_trait_change( self.trait_change, trait )

        return ((self.count > 0) or (len( self.traits ) > 0))

    #---------------------------------------------------------------------------
    #  Adds a new 'trait level' wiretap for an object:
    #---------------------------------------------------------------------------

    def add_trait ( self, object, trait, condition ):
        """ Adds a new trait specific wiretap for an object.
        """
        first = self.add_condition( trait, condition )
        if (self.count == 0) and first:
            object.on_trait_change( self.trait_change, trait )

    #---------------------------------------------------------------------------
    #  Removes a 'trait level' wiretap from an object:
    #---------------------------------------------------------------------------

    def remove_trait ( self, object, trait, condition ):
        """ Removes a trait specific wiretap from an object.
        """
        if ((not self.remove_condition( trait, condition )) and
            (self.count == 0)):
            object.on_trait_change( self.trait_change, trait, remove = True )

        return ((self.count > 0) or (len( self.traits ) > 0))

    #---------------------------------------------------------------------------
    #  Adds a condition to a specified trait:
    #---------------------------------------------------------------------------

    def add_condition ( self, trait, condition ):
        """ Adds a condition to a specified trait.
        """
        conditions = self.traits.setdefault( trait, {} )
        n          = len( conditions )
        items      = conditions.get( condition )
        if items is None:
            compiled = None
            if condition is not None:
                compiled = compile( condition, '<string>', 'eval' )
            conditions[ condition ] = items = [ compiled, 1 ]
        else:
            items[1] += 1

        return (n == 0)

    #---------------------------------------------------------------------------
    #  Removes a condition from a specified trait:
    #---------------------------------------------------------------------------

    def remove_condition ( self, trait, condition ):
        """ Removes a condition from a specified trait.
        """
        conditions = self.traits.get( trait )
        if conditions is not None:
            items = conditions.get( condition )
            if items is not None:
                items[1] -= 1
                if items[1] == 0:
                    del conditions[ condition ]
                    if len( conditions ) == 0:
                        del self.traits[ trait ]
                        return False

        return True

    #---------------------------------------------------------------------------
    #  Handles a trait of a monitored object being changed:
    #---------------------------------------------------------------------------

    def trait_change ( self, object, trait, old, new ):
        """ Handles any trait of a monitored object being changed.
        """
        if (self.if_condition( '', object ) or
            self.if_condition( trait, object )):
             fbi( "The monitored trait '%s' has been changed from %s to %s" %
                  ( trait, repr( old ), repr( new ) ), offset = 2 )

    #---------------------------------------------------------------------------
    #  Tests if any conditions for a specified trait are true:
    #---------------------------------------------------------------------------

    def if_condition ( myself, trait, self ):
        """ Tests if any conditions for a specified trait are true.
        """
        conditions = myself.traits.get( trait )
        if conditions is not None:
            for compiled, count in conditions.values():
                if (compiled is None) or eval( compiled ):
                    return True

        return False

#-------------------------------------------------------------------------------
#  'FBIWiretap' class:
#-------------------------------------------------------------------------------

class FBIWiretap ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Current objects being monitored:
    objects = Dict #( Str, Instance( Wiretap ) )

    #---------------------------------------------------------------------------
    #  Adds/Removes objects from the most wanted wiretap list:
    #---------------------------------------------------------------------------

    def wiretap ( self, monitor, remove ):
        """ Adds/Removes objects from the most wanted wiretap list.
        """
        # Normalize the 'monitor' value so that it is in the form of a list:
        if ((not isinstance( monitor, SequenceTypes )) or
            ((len( monitor ) > 1) and
             (isinstance( monitor[1], str ) or (monitor[1] is None)))):
            monitor = [ monitor ]

        # Process each item in the monitor list. Each item should have one of
        # the following forms:
        # - object
        # - ( object, )
        # - ( object, None )
        # - ( object, None, condition )
        # - ( object, trait )
        # - ( object, ( trait, ..., trait ) )
        # - ( object, trait, condition )
        # - ( object, ( trait, ..., trait ), condition )
        for item in monitor:
            traits = condition = None
            if not isinstance( item, SequenceTypes ):
                object = item
            else:
                n = len( item )
                if n == 0:
                    continue
                object = item[0]
                if n >= 2:
                    traits = item[1]
                    if ((traits is not None) and
                        (not isinstance( traits, SequenceTypes ))):
                        traits = [ traits ]
                    if n >= 3:
                        condition = item[2]
                        if condition == '':
                            condition = None

            if traits is None:
                self.wiretap_object( object, condition, remove )
            else:
                for trait in traits:
                    self.wiretap_trait( object, trait, condition, remove )

    #---------------------------------------------------------------------------
    #  Sets/Removes a wiretap on an entire object:
    #---------------------------------------------------------------------------

    def wiretap_object ( self, object, condition, remove ):
        """ Sets/Removes a wiretap on an entire object.
        """
        if remove:
            wiretap = self.get_wiretap_for( object, False )
            if ((wiretap is not None) and
                (not wiretap.remove_object( object, condition ))):
                del self.objects[ id( object ) ]
        else:
            self.get_wiretap_for( object ).add_object( object, condition )

    #---------------------------------------------------------------------------
    #  Sets/Removes a wiretap on a particular object trait, with an optional
    #  condition to be on the look-out for:
    #---------------------------------------------------------------------------

    def wiretap_trait ( self, object, trait, condition, remove ):
        """ Sets/Removes a wiretap on a particular object trait, with an
            optional condition to be on the look-out for.
        """
        if remove:
            wiretap = self.get_wiretap_for( object, False )
            if ((wiretap is not None) and
                (not wiretap.remove_trait( object, trait, condition ))):
                del self.objects[ id( object ) ]
        else:
            self.get_wiretap_for( object ).add_trait( object, trait, condition )

    #---------------------------------------------------------------------------
    #  Gets the Wiretap object for a specified object:
    #---------------------------------------------------------------------------

    def get_wiretap_for ( self, object, create = True ):
        """ Gets the Wiretap object for a specified object.
        """
        wiretap = self.objects.get( id( object ) )
        if (wiretap is None) and create:
            self.objects[ id( object ) ] = wiretap = Wiretap()

        return wiretap

# Create the FBI wiretap command center:
fbi_wiretap = FBIWiretap()

