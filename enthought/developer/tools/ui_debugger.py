#-------------------------------------------------------------------------------
#
#  Define an editor used to debug ui related problems.
#
#  Written by: David C. Morrill
#
#  Date: 09/27/2005
#
#  (c) Copyright 2005 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import wx

from enthought.traits.api \
    import HasPrivateTraits, Any, Instance, Property, Int, Str, List, Code, \
           TraitHandler, TraitError, Trait

from enthought.traits.ui.api \
    import View, HSplit, VSplit, VGroup, Item, TreeEditor, TreeNodeObject, \
           ObjectTreeNode, TableEditor, Handler
    
from enthought.traits.ui.table_column \
    import ObjectColumn

from enthought.traits.ui.menu \
    import NoButtons

from enthought.traits.ui.wx.editor \
    import Editor
    
from enthought.traits.ui.wx.basic_editor_factory \
    import BasicEditorFactory

from enthought.pyface.timer.api \
    import do_later
    
from enthought.developer.api \
    import HasPayload
    
#-------------------------------------------------------------------------------
#  Constants:  
#-------------------------------------------------------------------------------
        
# Map from wxPython bit to corresponding name:
all_flags = [ 
    ( wx.EXPAND,                  'EXPAND' ),
    ( wx.ALL,                     'ALL' ),
    ( wx.TOP,                     'TOP' ),
    ( wx.BOTTOM,                  'BOTTOM' ),
    ( wx.LEFT,                    'LEFT' ),
    ( wx.RIGHT,                   'RIGHT' ),
    ( wx.FIXED_MINSIZE,           'FIXED_MINSIZE' ),
    ( wx.ALIGN_CENTER,            'ALIGN_CENTER' ),
    ( wx.ALIGN_RIGHT,             'ALIGN_RIGHT' ),
    ( wx.ALIGN_BOTTOM,            'ALIGN_BOTTOM' ),
    ( wx.ALIGN_CENTER_VERTICAL,   'ALIGN_CENTER_VERTICAL' ),
    ( wx.ALIGN_CENTER_HORIZONTAL, 'ALIGN_CENTER_HORIZONTAL' )
]    
                                      
#-------------------------------------------------------------------------------
#  'UIDebugEditor' class:
#-------------------------------------------------------------------------------
                               
class UIDebugEditor ( Editor ):
        
    #---------------------------------------------------------------------------
    #  Finishes initializing the editor by creating the underlying toolkit
    #  widget:
    #---------------------------------------------------------------------------
        
    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        self.control = wx.Button( parent, -1, 'UI Debug...' )
        wx.EVT_BUTTON( parent, self.control.GetId(), self.update_object )
        self.set_tooltip()

    #---------------------------------------------------------------------------
    #  Handles the user entering input data in the edit control:
    #---------------------------------------------------------------------------
  
    def update_object ( self, event ):
        """ Handles the user entering input data in the edit control.
        """
        control = self.control
        while True:
            parent = control.GetParent()
            if parent is None:
                break
            control = parent
        UIDebugger(root = WXWindow( window = control ) ).edit_traits()
        
    #---------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #---------------------------------------------------------------------------
        
    def update_editor ( self ):
        """ Updates the editor when the object trait changes external to the 
            editor.
        """
        pass

#-------------------------------------------------------------------------------
#  Create the editor factory object:
#-------------------------------------------------------------------------------
                
ToolkitEditorFactory = BasicEditorFactory( klass = UIDebugEditor )

#-------------------------------------------------------------------------------
#  'SizerItem' class:  
#-------------------------------------------------------------------------------

class WXSizerItem ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
        
    item       = Instance( wx.SizerItem )
    kind       = Property
    calc_min   = Property
    proportion = Property
    flags      = Property
    border     = Property
    
    #---------------------------------------------------------------------------
    #  Property implementations:  
    #---------------------------------------------------------------------------
        
    def _get_kind ( self ):
        obj = self.item.GetWindow()
        if obj is not None:
            return obj.__class__.__name__
        return self.item.GetSizer().__class__.__name__
        
    def _get_calc_min ( self ):
        dx, dy = self.item.CalcMin()
        return str( ( dx, dy ) )
        
    def _get_proportion ( self ):
        return str( self.item.GetProportion() )
        
    def _get_flags ( self ):
        flags = self.item.GetFlag()
        names = []
        for bit, name in all_flags:
            if (flags & bit) == bit:
                names.append( name )
                flags &= ~bit
        if flags != 0:
            names.append( '%8X' % flags )
        return ', '.join( names )
        
    def _get_border ( self ):
        return str( self.item.GetBorder() )
        
#-------------------------------------------------------------------------------
#  Tabele editor to use for displaying Sizer item information:  
#-------------------------------------------------------------------------------
        
sizer_item_table_editor = TableEditor(        
    columns = [ ObjectColumn( name = 'kind',       editable = False ),
                ObjectColumn( name = 'calc_min',   editable = False ),
                ObjectColumn( name = 'proportion', editable = False ),
                ObjectColumn( name = 'border',     editable = False ),
                ObjectColumn( name = 'flags',      editable = False ) ],
    editable     = False,
    configurable = False,
    sortable     = False
)
    
#-------------------------------------------------------------------------------
#  'WXWindow' class:  
#-------------------------------------------------------------------------------
        
class WXWindow ( TreeNodeObject ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
        
    window    = Instance( wx.Window )
    name      = Property
    position  = Property
    size      = Property
    sizer     = Property
    min_size  = Property
    best_size = Property
    items     = Property( List )
    result    = Property( Code )
    evaluate  = Str
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------
        
    view = View( 
        VSplit(
            VGroup( 'position~', 'size~', 'sizer~', 'min_size~', 'best_size~',
                    label = 'Information',
                    dock  = 'horizontal' ),
            Item( 'items',
                  label      = 'Sizer Children',
                  show_label = False,
                  editor     = sizer_item_table_editor,
                  dock       = 'horizontal' ),
            VGroup( 'evaluate', 'result#~',
                    label = 'Evaluate',
                    dock  = 'horizontal' ),
            id = 'splitter'
        ),
        id   = 'enthought.developer.tools.ui_debugger.item',
        kind = 'subpanel' 
    )
                 
    #---------------------------------------------------------------------------
    #  Handles 'evaluate' being changed:
    #---------------------------------------------------------------------------
                                  
    def _evaluate_changed ( self ):
        self.trait_property_changed( 'result', None, None )
    
    #---------------------------------------------------------------------------
    #  Implementation of the various trait properties:  
    #---------------------------------------------------------------------------
        
    def _get_name ( self ):
        w = self.window
        try:
            label = w.GetLabel()
        except:
            try:
                label = w.GetValue()
            except:
                try:
                    label = w.GetTitle()
                except:
                    label = ''
        if label != '':
            label = ' (%s)' % label
        return self.window.__class__.__name__ + label
        
    def _get_size ( self ):
        dx, dy = self.window.GetSizeTuple()
        return str( ( dx, dy ) )
        
    def _get_position ( self ):
        x, y = self.window.GetPositionTuple()
        return str( ( x, y ) )
        
    def _get_sizer ( self ):
        sizer = self.window.GetSizer()
        if sizer is None:
            return ''
        dx, dy = sizer.CalcMin()
        return '%s( %d, %d )' % ( sizer.__class__.__name__, dx, dy )
        
    def _get_min_size ( self ):
        dx, dy = self.window.GetMinSize()
        return str( ( dx, dy ) )
        
    def _get_best_size ( self ):
        dx, dy = self.window.GetBestFittingSize()
        return str( ( dx, dy ) )
                                  
    def _get_result ( self ):
        try:
            result = eval( self.evaluate, { '_':  self.window,
                                            '__': self.window.GetSizer() } )
            if isinstance( result, ( list, tuple ) ):
                return '\n'.join( [ '[%d]: %s' % ( i, str( x ) ) 
                                      for i, x in enumerate( result ) ] )
            return str( result )
        except:
            return '???'
            
    def _get_items ( self ):
        sizer = self.window.GetSizer()
        if sizer is None:
            return []
        items = []
        try:
            for i in range( 10000 ):
                item = sizer.GetItem( i )
                if item is None:
                    break
                items.append( WXSizerItem( item = item ) )
        except:
            pass
        return items

    #---------------------------------------------------------------------------
    #  Returns whether chidren of this object are allowed or not:  
    #---------------------------------------------------------------------------

    def tno_allows_children ( self, node ):
        """ Returns whether chidren of this object are allowed or not.
        """
        return True
    
    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:  
    #---------------------------------------------------------------------------

    def tno_has_children ( self, node = None ):
        """ Returns whether or not the object has children.
        """
        return (len( self.window.GetChildren() ) > 0)
        
    #---------------------------------------------------------------------------
    #  Gets the object's children:  
    #---------------------------------------------------------------------------

    def tno_get_children ( self, node ):
        """ Gets the object's children.
        """
        return [ WXWindow( window = window ) 
                 for window in self.window.GetChildren() ]
        
    #---------------------------------------------------------------------------
    #  Returns the 'draggable' version of a specified object:  
    #---------------------------------------------------------------------------
                
    def tno_get_drag_object ( self, node ):
        """ Returns the 'draggable' version of a specified object.
        """
        return self.window
    
#-------------------------------------------------------------------------------
#  Defines the window browser tree editor:  
#-------------------------------------------------------------------------------
        
window_tree_editor = TreeEditor(
    nodes = [
        ObjectTreeNode( node_for = [ WXWindow ],
                        children = 'children',
                        label    = 'name' ),
    ],
    selected = 'selected',
    editable = False
)

#-------------------------------------------------------------------------------
#  'WindowPayloadHandler' class:
#-------------------------------------------------------------------------------

class WindowPayloadHandler ( TraitHandler ):

    #---------------------------------------------------------------------------
    #  Verifies that a specified value is valid for a trait:  
    #---------------------------------------------------------------------------

    def validate ( self, object, name, value ):
        """ Verifies that a specified value is valid for a trait.
        """
        if value is None:
            return None
            
        if isinstance( value, wx.Window ):
            return value
            
        if (isinstance( value, HasPayload ) and 
            isinstance( value.payload, wx.Window )):
            return value.payload
            
        raise TraitError
        
#-------------------------------------------------------------------------------
#  'UIDebugger' class:  
#-------------------------------------------------------------------------------

class UIDebugger ( Handler ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
    
    # The name of the plugin:
    name = Str( 'UI Debugger' )
    
    # The current wx Window being 'debugged':
    window = Trait( None, WindowPayloadHandler(),
                    droppable = 'Drop a wx.Window object here.' )
    
    # Root of a wxWindow window hierarchy:
    root = Instance( WXWindow, allow_none = True )
    
    # The currently selected window:
    selected = Instance( WXWindow, allow_none = True )
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------
        
    view = View(
        HSplit(
            Item( 'root',
                  label      = 'Hierarchy',
                  show_label = False,
                  editor     = window_tree_editor,
                  resizable  = True,
                  dock       = 'horizontal' ),
            Item( 'selected@',
                  id         = 'selected',
                  label      = 'Selected',
                  show_label = False,
                  resizable  = True,
                  dock       = 'horizontal' ),
            id = 'splitter'
        ),
        title = 'UI Debugger',
        id    = 'enthought.developer.tools.ui_debugger'
    )
        
    #---------------------------------------------------------------------------
    #  Handles the 'window' trait being changed:
    #---------------------------------------------------------------------------
    
    def _window_changed ( self, window ):
        if window is not None:
            self.root = WXWindow( window = window )
            do_later( self.set, window = None )
                
#-------------------------------------------------------------------------------
#  Create export objects:
#-------------------------------------------------------------------------------

view = UIDebugger()
    
