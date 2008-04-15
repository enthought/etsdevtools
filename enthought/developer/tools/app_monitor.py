#-------------------------------------------------------------------------------
#  
#  Application Monitor plugin
#  
#  Written by: David C. Morrill
#  
#  Date: 07/16/2006
#  
#  (c) Copyright 2006 by David C. Morrill
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------
    
from enthought.traits.api \
    import HasTraits, HasPrivateTraits, Str, Instance, List, Enum, Property
    
from enthought.traits.ui.api \
    import View, Item, ValueEditor, ListEditor
    
from enthought.pyface.dock.api \
    import DockControl
 
try:    
    from enthought.envisage import get_application
except:
    get_application = None
    
from enthought.pyface.image_resource \
    import ImageResource
    
from enthought.developer.features.api \
    import CustomFeature
    
#-------------------------------------------------------------------------------
#  'AppMonitor' plugin:
#-------------------------------------------------------------------------------

class AppMonitor ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Application Monitor' )
    
    # The persistence id for this object:
    id = Str( 'enthought.developer.tools.app_monitor.state',
              save_state_id = True )
    
    # The view style used to display the data:
    view_style = Enum( 'Tree', 'Notebook', save_state = True )
    
    feature = Instance( CustomFeature, {
                            'image':   ImageResource( 'refresh' ),
                            'click':   'refresh',
                            'tooltip': 'Click to refresh view.'
                        },
                        custom_feature = True )

    # Our DockControl object:
    dock_control = Instance( DockControl, dock_control = True )
    
    # The list of application objects being monitored:
    objects = List
    
    # The current view_object:
    view_object = Instance( HasTraits )
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( 'view_object@', 
              show_label = False,
              resizable  = True
        )
    )
    
    options = View(
        Item( 'view_style', width = 180 ),
        title   = 'Application Monitor Options',
        id      = 'enthought.developer.tools.app_monitor.options',
        buttons = [ 'OK', 'Cancel' ]
    )
        
    #---------------------------------------------------------------------------
    #  Refreshes the contents of the view:  
    #---------------------------------------------------------------------------

    def refresh ( self ):
        """ Refreshes the contents of the view.
        """
        global get_application
        
        self.objects = [ dc.object for dc in self.dock_control.dock_controls
                                  if isinstance( dc.object, HasTraits ) ]
        if get_application is not None:
            self.objects.append( get_application() )
        self.set_view_object()
        
    #---------------------------------------------------------------------------
    #  Handles the 'dock_control' trait being changed:  
    #---------------------------------------------------------------------------

    def _dock_control_changed ( self ):
        """ Handles the 'dock_control' trait being changed.
        """
        self.refresh()
                          
    #---------------------------------------------------------------------------
    #  Handles the 'view_style' trait being changed:  
    #---------------------------------------------------------------------------
    
    def _view_style_changed ( self ):
        """ Handles the 'view_style' trait being changed.
        """
        self.set_view_object()
        
    #---------------------------------------------------------------------------
    #  Sets the current view object based on the current view style:  
    #---------------------------------------------------------------------------

    def set_view_object ( self ):
        """ Sets the current view object based on the current view style.
        """
        if self.view_style == 'Tree':
            self.view_object = AppTreeView( objects = self.objects )
        else:
            self.view_object = AppNotebookView( objects = self.objects )
                          
#-------------------------------------------------------------------------------
#  'AppTreeView' class:
#-------------------------------------------------------------------------------

class AppTreeView ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:    
    #---------------------------------------------------------------------------

    # The list of objects to display:
    objects = List
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( 'objects', 
              show_label = False,
              editor     = ValueEditor()
        )
    )
                          
#-------------------------------------------------------------------------------
#  'AppNotebookView' class:
#-------------------------------------------------------------------------------

class AppNotebookView ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:    
    #---------------------------------------------------------------------------

    # The list of objects to display:
    objects = List
    
    # The list of NotebookItems corresponding to the list of objects:
    items = List
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( 'items@',
              show_label = False,
              editor     = ListEditor( use_notebook = True,
                                       deletable    = True,
                                       page_name    = '.name',
                                       export       = 'DockWindowShell',
                                       dock_style   = 'tab' )
        )
    )
    
    #---------------------------------------------------------------------------
    #  Handles the 'objects' trait being changed:  
    #---------------------------------------------------------------------------
    
    def _objects_changed ( self, objects ):
        """ Handles the 'objects' trait being changed.
        """
        self.items = [ NotebookItem( object = object ) for object in objects ]

#-------------------------------------------------------------------------------
#  'NotebookItem' class:
#-------------------------------------------------------------------------------

class NotebookItem ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------

    # The object being displayed:
    object = Instance( HasTraits )
    
    # The name of the object:
    name = Property
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( 'object', 
              show_label = False,
              editor     = ValueEditor()
        )
    )
    
    #---------------------------------------------------------------------------
    #  Implementation of the 'name' property:  
    #---------------------------------------------------------------------------

    def _get_name ( self ):
        return self.object.__class__.__name__
    
#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = AppMonitor()
        
