#-------------------------------------------------------------------------------
#  
#  A custom editor for grabbing wxWindow windows.
#  
#  Written by: David C. Morrill
#  
#  Date: 08/28/2008
#  
#  (c) Copyright 2008 by Enthought, Inc.                                      
#  
#-------------------------------------------------------------------------------

""" A custom editor for grabbing wxWindow windows.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------
  
import wx  
    
from enthought.traits.api \
    import Bool, Instance, Str, on_trait_change
    
from enthought.traits.ui.api \
    import Image
    
from enthought.traits.ui.basic_editor_factory \
    import BasicEditorFactory
    
from enthought.traits.ui.wx.editor \
    import Editor       

from enthought.traits.ui.wx.themed_control \
    import ThemedControl
    
#-------------------------------------------------------------------------------
#  'WindowGrabber' class:
#-------------------------------------------------------------------------------    

class WindowGrabber ( ThemedControl ):
    """ Defines a control that can be used to grab other wxPython windows.
    """
    
    # The most recent window selected:
    selected = Instance( wx.Window )
    
    # The most recent window the mouse pointer passed over:
    over = Instance( wx.Window )
    
    # The image to be drawn inside the control:
    image = Image( 'window_grabber_inactive' )
    
    # The image to display when inactive:
    image_inactive = Image( 'window_grabber_inactive' )
    
    # The image to display when the mouse is hovering over the editor:
    image_hover = Image( 'window_grabber_hover' )
    
    # The image to display when active but not over a valid window:
    image_tracking = Image( 'window_grabber_tracking' )
    
    # The image to display when active and over a valid window:
    image_locked = Image( 'window_grabber_locked' )
    
    #-- wxPython Event Handlers ------------------------------------------------
    
    def normal_enter ( self, x, y, event ):
        self.image = self.image_hover
        
    def normal_leave ( self, x, y, event ):
        self.image = self.image_inactive
        
    def normal_left_down ( self, x, y, event ):
        self.state = 'tracking'
        self.image = self.image_tracking
        self.control.SetCursor( wx.StockCursor( wx.CURSOR_QUESTION_ARROW ) )
        
    def tracking_left_up ( self, x, y, event ):
        self.state    = 'normal'
        self.selected = self._get_window_at( x, y )
        self.image    = self.image_inactive
        self.control.SetCursor( wx.NullCursor )
        
    def tracking_motion ( self, x, y, event ):
        self.over = self._get_window_at( x, y )
        if self.over is None:
            self.image = self.image_tracking
        else:
            self.image = self.image_locked

    #-- Private Methods --------------------------------------------------------
    
    def _get_window_at ( self, x, y ):
        """ Locates the wxPython at the specified window coordinates (if any).
        """
        window = wx.FindWindowAtPoint( self.control.ClientToScreenXY( x, y ) )
        if window is self.control:
            window = None
            
        return window
    
#-------------------------------------------------------------------------------
#  '_WindowGrabberEditor' class:
#-------------------------------------------------------------------------------

class _WindowGrabberEditor ( Editor ):
    """ A custom editor for Margin/Border instances.
    """
    
    # The WindowGrabber control we are using to implement the editor:
    grabber = Instance( WindowGrabber, () )
    
    # The most recent window the mouse pointer passed over:
    over = Instance( wx.Window )

    #-- Editor Methods ---------------------------------------------------------
    
    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        self.control = self.grabber.create_control( parent )
        self.sync_value( self.factory.over, 'over', 'to' ) 
        self.set_tooltip()
        
    def update_editor ( self ):
        """ Handles the trait bound to the editor being updated.
        """
        pass
    
    #-- Traits Event Handlers --------------------------------------------------
    
    @on_trait_change( 'grabber:selected' )
    def _selected_modified ( self, window ):
        self.value = window
    
    @on_trait_change( 'grabber:over' )
    def _over_modified ( self, window ):
        self.over = window

#-------------------------------------------------------------------------------
#  Create the editor factory object:
#-------------------------------------------------------------------------------

# Editor factory for the WindowGrabberEditor:

class WindowGrabberEditor ( BasicEditorFactory ):
    
    # The editor class to be created:
    klass = _WindowGrabberEditor
    
    # The extended trait name to synchronize the most recent window passed over
    # by the WindowGrabber with:
    over = Str
    
