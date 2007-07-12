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
#  (c) Copyright 2006 by Enthought, Inc.
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
    import split, join, isdir

from bdb \
    import Bdb

from traceback \
    import format_tb

from enthought.traits.api \
    import HasTraits, HasPrivateTraits, Str, Int, Instance, List, Dict, Any, \
           Code, Constant, Property, PythonValue, true, false, Button, \
           Event, TraitError
from enthought.traits.ui.api \
    import View, VSplit, VGroup, HSplit, HGroup, HFlow, Tabbed, Item, \
           TableEditor, ValueEditor, CodeEditor, InstanceEditor, TextEditor, \
           EnumEditor, Handler, UI

from enthought.traits.ui.value_tree \
    import ValueTree

from enthought.traits.ui.menu \
    import NoButtons

from enthought.traits.ui.table_column \
    import ObjectColumn

from enthought.pyface.image_resource \
    import ImageResource

from enthought.traits.vet.class_browser \
    import ClassBrowser, ClassBrowserPaths, CBPath

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
#  'BreakPoint' class:
#-------------------------------------------------------------------------------

class BreakPoint ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # File containing the break point:
    file_name = Str

    # File path for the file containing the break point:
    file_path = Str

    # Line number within the file the break point is on:
    line = Int

    # Is the break point enabled?
    enabled = true

    # Is the break point temporary (i.e. a one shot)?
    temporary = false

    # Optional conditional expression specifying when the break point should
    # stop:
    condition = Str

    # Source line:
    source = Str

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

    # File path for the file defining the module:
    file_path = Str

    # List of the line numbers of the active break points in the module:
    bp_lines = List( Int )

#-------------------------------------------------------------------------------
#  FBIValue table editor definition:
#-------------------------------------------------------------------------------

fbi_value_editor = TableEditor(
    columns   = [ ObjectColumn( name     = 'name',
                                editable = False ),
                  ObjectColumn( name     = 'type',
                                editable = False,
                                horizontal_alignment = 'center' ),
                  ObjectColumn( name     = 'str_value',
                                label    = 'Value',
                                editable = False ),
                ],
    selection_bg_color = SelectionColor,
    selection_color    = 'black',
    editable           = False,
    auto_size          = False
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

    # Current break point line number:
    bp_line = Event

    # List of lines containing break points:
    bp_lines = List( Int )

    # Should a break point be only temporary?
    temporary = false

    # Optional condition to apply to break point:
    condition = Str

    # Error message returned by 'bdb' when setting a break point:
    msg = Str

    # Source code line being executed:
    source = Str

    # Module source code:
    module_source = Code

    # List of local variables (including the arguments):
    local_variables = List( FBIValue )

    # Currently selected local variable:
    variable = Any

    # Python shell values:
    shell_values = PythonValue

    #---------------------------------------------------------------------------
    #  Trait view definitions:
    #---------------------------------------------------------------------------

    view = View(
              VSplit(
                  Item( 'local_variables',
                        label  = 'Local Variables',
                        id     = 'local_variables',
                        export = 'DockShellWindow',
                        editor = fbi_value_editor ),
                  HSplit(
                      Tabbed(
                          Item( 'shell_values',
                                label  = 'Python Shell',
                                export = 'DockShellWindow' ),
                          Item( 'variable',
                                label  = 'Variable Value',
                                export = 'DockShellWindow',
                                editor = ValueEditor() ),
                          show_labels = False
                      ),
                      VGroup(
                          HGroup(
                              HGroup( 'temporary{Temporary break point}',
                                      show_left = False ), '_',
                              'condition<150>', '_',
                              Item( 'msg~', show_label = False )
                          ),
                          VGroup(
                          Item( 'module_source~',
                                show_label = False,
                                editor = CodeEditor( selected_line = 'line',
                                                     mark_lines = 'bp_lines',
                                                     mark_color = SelectionColor,
                                                     line       = 'bp_line' )
                          ) ),
                          id     = 'module',
                          label  = 'Module Source',
                          export = 'DockShellWindow'
                      ),
                      show_labels = False
                  ),
                  id          = 'splitter',
                  show_labels = False
              ),
              id   = 'enthought.debug.fbi.stack_frame',
              dock = 'tab'
           )

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, stack_frame ):
        """ Initializes the object.
        """
        frame, file_name, line, self.function_name, lines, index = stack_frame
        self.file_path, self.file_name = split( file_name )

        # Create the list of local variables:
        locals  = self.variable = self.shell_values = frame.f_locals
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
        fh = None
        try:
            fh = open( file_name, 'rb' )
            self.module_source = fh.read()
        except:
            pass
        if fh is not None:
            fh.close()

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

stack_frame_editor = TableEditor(
    columns   = [ ObjectColumn( name     = 'function_name',
                                label    = 'Function',
                                editable = False ),
                  ObjectColumn( name     = 'file_name',
                                label    = 'File Name',
                                editable = False ),
                  ObjectColumn( name     = 'file_path',
                                label    = 'File Path',
                                editable = False ),
                  ObjectColumn( name     = 'line',
                                editable = False,
                                horizontal_alignment = 'center' ),
                  ObjectColumn( name     = 'source',
                                editable = False ),
                ],

    selection_bg_color = SelectionColor,
    selection_color    = 'black',
    configurable       = False,
    editable           = False,
    auto_size          = False,
    sortable           = False,
    on_select          = 'object.select_frame'
)

#-------------------------------------------------------------------------------
#  'TemporaryColumn' class:
#-------------------------------------------------------------------------------

class TemporaryColumn ( ObjectColumn ):

    #---------------------------------------------------------------------------
    #  Gets the value of the column for a specified object:
    #---------------------------------------------------------------------------

    def get_value ( self, object ):
        """ Gets the value of the column for a specified object.
        """
        if getattr( object, self.name ):
            return 'Yes'
        return ''

#-------------------------------------------------------------------------------
#  Break points table editor definition:
#-------------------------------------------------------------------------------

bp_table_editor = TableEditor(
    columns   = [ #ObjectColumn( name     = 'enabled',
                  #              label    = 'Enabled?' ),
                  ObjectColumn( name     = 'file_name',
                                label    = 'File Name',
                                editable = False ),
                  ObjectColumn( name     = 'file_path',
                                label    = 'File Path',
                                editable = False ),
                  ObjectColumn( name     = 'line',
                                editable = False,
                                horizontal_alignment = 'center' ),
                  TemporaryColumn( name     = 'temporary',
                                editable = False,
                                horizontal_alignment = 'center' ),
                  ObjectColumn( name     = 'condition',
                                editable = False ),
                  ObjectColumn( name     = 'source',
                                editable = False ),
                ],
    selection_bg_color = SelectionColor,
    selection_color    = 'black',
    configurable       = True,
    editable           = True,
    auto_size          = False,
    sortable           = True
)

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
        fbi( msg = 'Step', offset = 3, debug_frame = frame )

    def user_return ( self, frame, return_value ):
        """ This method is called when a return trap is set here.
        """
        fbi( msg = 'Return', offset = 3, debug_frame = frame )

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

    def do_clear ( self, bp_number ):
        self.clear_bpbynumber( bp_number )

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
    frame = Instance( StackFrame )

    # A scatch pad area for accumulating interesting values to look at:
    value_tree = ValueTree

    # The list of currently defined break points:
    break_points = List( Instance( BreakPoint ) )

    # List of currently active data watches:
    data_watches = List( Instance( DataWatch ) )

    # The list of modules containing break point information:
    modules = List( Instance( FBIModule ) )

    # A class browser:
    class_browser = Constant( TheClassBrowser )

    # The text version of the traceback from the most recent exception caught:
    traceback = Str

    # Ignore the next request to set a break point?
    ignore_bp = false

    # Is the FBI being run under an app that has a UI:
    has_ui = true

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
                   HFlow( Item( 'step<80>@',
                                enabled_when = 'debug_frame is not None' ),
                          Item( 'next<80>@',
                                enabled_when = 'debug_frame is not None' ),
                          Item( 'ret<80>@',
                                enabled_when = 'debug_frame is not None' ),
                          Item( 'go<80>@',
                                enabled_when = 'debug_frame is not None' ),
                          Item( 'quit<80>@',
                                enabled_when = 'debug_frame is not None' ),
                          dock        = 'horizontal',
                          label       = 'Toolbar',
                          show_labels = False ),
                   VGroup( 'msg~',
                           dock        = 'vertical',
                           label       = 'Status',
                           show_labels = False ),
                   Tabbed(
                       Item( 'frames',
                             label  = 'Stack Frames',
                             id     = 'frames',
                             editor = stack_frame_editor
                       ),
                       Item( 'break_points',
                             label  = 'Break Points',
                             id     = 'break_points',
                             editor = bp_table_editor ),
                       Item( 'data_watches',
                             label  = 'Data Watches',
                             id     = 'data_watches',
                             editor = dw_table_editor ),
                       Item( 'value_tree',
                             label  = 'Watch Values',
                             export = 'DockShellwindow' ),
                       Item( 'class_browser@',
                             label  = 'Class Browser',
                             id     = 'class_browser',
                             editor = InstanceEditor(
                                          view = 'imbedded_source_view' ),
                             export = 'DockShellWindow' ),
                       Item( 'traceback@',
                             label  = 'Traceback',
                             id     = 'traceback',
                             editor = TextEditor( multi_line = True ),
                             export = 'DockWindowShell' ),
                       show_labels = False
                   ),
                   Item( 'frame@',
                         dock   = 'horizontal',
                         id     = 'frame',
                         export = 'DockShellWindow' ),
                   id          = 'splitter',
                   show_labels = False
               ),
               title     = 'FBI: Frame Based Inspector',
               id        = 'enthought.debug.fbi.fbi',
               kind      = 'livemodal',
               dock      = 'tab',
               width     = 0.8,
               height    = 0.8,
               resizable = True,
               buttons   = NoButtons
           )

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, **traits ):
        """ Initializes the object.
        """
        super( FBI, self ).__init__( **traits )
        if len( self.frames ) == 0:
            self.frames = [ StackFrame( frame ) for frame in stack( 15 )[1:] ]

    #---------------------------------------------------------------------------
    #  Initializes the controls of a user interface:
    #---------------------------------------------------------------------------

    def init ( self, info ):
        """ Initializes the controls of a user interface.
        """
        self.ui = info.ui

    #---------------------------------------------------------------------------
    #  Handles the 'frames' trait being changed:
    #---------------------------------------------------------------------------

    def _frames_changed ( self, frames ):
        """ Handles the 'frames' trait being changed.
        """
        if len( frames ) > 0:
            self.ignore_bp = True
            self.frame     = frame = frames[0]
            i, bp          = self.get_break_point_for( frame, frame.line )
            if (bp is not None) and bp.temporary:
                del self.break_points[i]
                frame.bp_lines.remove( frame.line )
                self.get_module_for( frame ).bp_lines.remove( frame.line )

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
        self.debug_frame = None
        self.ui.control.EndModal( True )

    #---------------------------------------------------------------------------
    #  Handles the user selecting a new stack frame:
    #---------------------------------------------------------------------------

    def select_frame ( self, frame ):
        """ Handles the user selecting a new stack frame.
        """
        self.ignore_bp = True
        self.frame     = frame

    #---------------------------------------------------------------------------
    #  Handles the 'frame' trait being changed:
    #---------------------------------------------------------------------------

    def _frame_changed ( self, old, new ):
        """ Handles the 'frame' trait being changed.
        """
        if old is not None:
            old.on_trait_change( self.set_break_point, 'bp_line',
                                 remove = True )
        if new is not None:
            new.on_trait_change( self.set_break_point, 'bp_line' )
            new.bp_lines = self.get_module_for( new ).bp_lines

    #---------------------------------------------------------------------------
    #  Sets/Unsets a breakpoint when the user clicks a line in the module
    #  source view:
    #---------------------------------------------------------------------------

    def set_break_point ( self, line ):
        """ Sets/Unsets a breakpoint when the user clicks a line in the module
            source view.
        """
        frame = self.frame
        if self.ignore_bp:
            self.ignore_bp = False
            return

        file_name = frame.file_name
        file_path = frame.file_path
        module    = self.get_module_for( frame )
        i, bp     = self.get_break_point_for( frame, line )
        if bp is not None:
            fbi_bdb.clear_break( join( file_path, file_name ), line )
            del self.break_points[i]
            frame.bp_lines.remove(  line )
            module.bp_lines.remove( line )
            if ((bp.temporary != frame.temporary) or
                (bp.condition != frame.condition)):
                bp = None

        if bp is None:
            msg = fbi_bdb.set_break( join( file_path, file_name ), line,
                                     frame.temporary, frame.condition )
            if msg is None:
                self.break_points.append(
                    BreakPoint( file_name = file_name,
                                file_path = file_path,
                                line      = line,
                                temporary = frame.temporary,
                                condition = frame.condition,
                                source    = frame.module_source.split(
                                                '\n' )[ line - 1 ].strip() ) )
                frame.bp_lines.append(  line )
                module.bp_lines.append( line )
                frame.condition = ''
            else:
                self.msg = msg

    #---------------------------------------------------------------------------
    #  Gets the FBIModule corresponding to a specified frame:
    #---------------------------------------------------------------------------

    def get_module_for ( self, frame ):
        """ Gets the FBIModule corresponding to a specified frame.
        """
        for module in self.modules:
            if ((frame.file_path == module.file_path) and
                (frame.file_name == module.file_name)):
                return module

        module = FBIModule( file_path = frame.file_path,
                            file_name = frame.file_name )
        self.modules.append( module )
        return module

    #---------------------------------------------------------------------------
    #  Returns the break point (if any) at a specified frame line:
    #---------------------------------------------------------------------------

    def get_break_point_for ( self, frame, line ):
        """ Returns the break point (if any) at a specified frame line.
        """
        for i, bp in enumerate( self.break_points ):
            if ((frame.file_name == bp.file_name) and
                (frame.file_path == bp.file_path) and
                (line            == bp.line)):
                return ( i, bp )

        return ( None, None )

#---------------------------------------------------------------------------
#  Enables/Disables FBI to handle unhandled exceptions:
#---------------------------------------------------------------------------

# Global flag indicating whether or not the FBI is enabled:
fbi_enabled = False

# Does the application have a GUI interface?
has_gui = True

# Original 'sys.excepthook' handler:
saved_excepthook = None

# The FBI window:
fbi_object = None
fbi_ui     = None

def enable_fbi ( enabled = True, gui = True ):
    """ Enables/Disables FBI to handle unhandled exceptions.
    """
    global fbi_enabled, has_gui, saved_excepthook

    fbi_enabled = enabled
    has_gui     = gui
    if enabled:
        sys.excepthook, saved_excepthook = fbi_exception, sys.excepthook

def fbi_exception ( type, value, traceback, msg = '', gui = None, offset = 0,
                    debug_frame = None ):
    global fbi_object, fbi_ui, fbi_enabled, has_gui, saved_excepthook

    if gui is not None:
        has_gui = gui

    if value is None:
        if msg == '':
            msg = 'Called the FBI'
        frames = [ StackFrame( frame ) for frame in stack( 15 )[ offset + 2: ] ]
    else:
        if msg == '':
            msg = 'Exception: %s' % str( value )
        frames = [ StackFrame( frame )
                   for frame in getinnerframes( traceback, 15 ) ]
        frames.reverse()
        frames.extend( [ StackFrame( frame ) for frame in stack( 15 )[3:] ] )

    enabled = fbi_enabled
    if enabled:
        fbi_enabled    = False
        sys.excepthook = saved_excepthook

    # Format the text of the exception traceback (if any):
    tb = ''.join( format_tb( traceback ) )+msg

    if fbi_ui is None:
        if has_gui:
            fbi_object = FBI( msg         = msg,
                              frames      = frames,
                              debug_frame = debug_frame,
                              traceback   = tb )
            fbi_ui = fbi_object.edit_traits()
            if fbi_ui.control is None:
                fbi_ui = None
        else:
            FBI( msg         = msg,
                 frames      = frames,
                 debug_frame = debug_frame,
                 traceback   = tb,
                 has_ui      = False ).configure_traits()
            has_gui = False
    else:
        fbi_object.set( msg = msg, frames = frames, debug_frame = debug_frame,
                        traceback = tb )
        fbi_ui.control.ShowModal()
        if fbi_ui.control is None:
            fbi_ui = None

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
          offset = 0, debug_frame = None ):
    """ Creates and displays an FBI object.
    """
    global fbi_wiretap, has_gui

    if monitor is not None:
        if gui is not None:
            has_gui = gui
        fbi_wiretap.wiretap( monitor, remove )
    elif stop:
        fbi_exception( msg         = msg,
                       gui         = gui,
                       offset      = offset,
                       debug_frame = debug_frame,
                       *sys.exc_info() )

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

