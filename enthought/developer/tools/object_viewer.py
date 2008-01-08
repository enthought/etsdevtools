#-------------------------------------------------------------------------------
#  
#  Object Viewer plugin
#  
#  Written by: David C. Morrill
#  
#  Date: 07/29/2006
#  
#  (c) Copyright 2006 by David C. Morrill
#  
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------
    
from enthought.traits.api \
    import HasTraits, HasPrivateTraits, Any, Str, List, Range, Instance
    
from enthought.traits.ui.api \
    import View, VGroup, Item, ListEditor, InstanceEditor
    
from enthought.pyface.timer.api \
    import do_later
           
from enthought.developer.api \
    import HasPayload
           
from enthought.developer.helper.themes \
    import TTitle
    
#-------------------------------------------------------------------------------
#  'ObjectViewer' plugin:
#-------------------------------------------------------------------------------

class ObjectViewer ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Object Viewer' )
    
    # The persistence id for this object:
    id = Str( 'enthought.developer.tools.object_viewer.state',
              save_state_id = True )
    
    # Maximum number of open viewers allowed:
    max_viewers = Range( 1, 50, 50, mode = 'spinner', save_state = True )

    # The current item being viewed:
    object = Instance( HasTraits,
                      droppable = 'Drop an object with traits here to view it.',
                      connect   = 'to: object with traits' )
    
    # Current list of objects viewed:
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
                                       dock_style   = 'tab' )
        )
    )
    
    options = View(
        Item( 'max_viewers',
              label = 'Maximum number of open viewers',
              width = -50
        ),
        title   = 'Object Viewer Options',
        id      = 'enthought.developer.tools.object_viewer.options',
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
    #  Handles the 'object' trait being changed:    
    #---------------------------------------------------------------------------

    def _object_changed ( self, object ):
        """ Handles the 'object' trait being changed.
        """
        if object is not None:
            # Reset the current object to None, so we are ready for a new one:
            do_later( self.set, object = None )
            
            name = title = ''
            if isinstance( object, HasPayload ):
                name   = object.payload_name
                title  = object.payload_full_name
                object = object.payload
            
            viewers = self.viewers
            for i, viewer in enumerate( viewers ):
                if object is viewer.object:
                    if i == (len( viewers ) - 1):
                        return
                    del viewers[i]
                    break
            else:            
                # Create the viewer:
                viewer = AnObjectViewer( name   = name,
                                         title  = title ).set(
                                         object = object )
                
                # Make sure the # of viewers doesn't exceed the maximum allowed:
                if len( viewers ) >= self.max_viewers:
                    del viewers[0]
                
            # Add the new viewer to the list of viewers (which will cause it to 
            # appear as a new notebook page):
            viewers.append( viewer )

#-------------------------------------------------------------------------------
#  'AnObjectViewer' class:
#-------------------------------------------------------------------------------

class AnObjectViewer ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------

    # The viewer page name:
    name = Str
    
    # The object associated with this view:
    object = Any
    
    # The title of this view:
    title = Str
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------

    view = View(
        VGroup( 
            TTitle( 'title', visible_when = "title != ''" ),
            Item( 'object@', editor = InstanceEditor() ),
            show_labels = False
        )
    )

    #---------------------------------------------------------------------------
    #  Updates the 'object' trait being changed:
    #---------------------------------------------------------------------------

    def _object_changed ( self, object ):
        """ Updates the 'object' trait being changed.
        """
        if self.name == '':
            try:
                name = getattr( object, 'name', None )
                if not isinstance( name, str ):
                    name = None
            except:
                name = None
            
            if name is None:
                name = object.__class__.__name__
            
            self.name = name
        
        if self.title == '':
            try:
                self.title = getattr( object, 'title', None )
            except:
                pass
        
#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = ObjectViewer()
        
