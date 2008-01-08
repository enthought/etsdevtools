#-------------------------------------------------------------------------------
#  
#  Extension point adapters for ExtensionPoint subclasses defined in: 
#  - enthought.envisage.workbench.workbench_plugin_definition.py
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

from enthought.traits.ui.api \
    import VGroup, HGroup, Item
    
from enthought.developer.tools.envisage_browser.object_adapter \
    import Export

from enthought.developer.tools.envisage_browser.extension_point_adapter \
    import ExtensionPointAdapter
    
#-------------------------------------------------------------------------------
#  'WorkbenchAdapter' class:
#-------------------------------------------------------------------------------

class WorkbenchAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:    
    #---------------------------------------------------------------------------
    
    default_perspective = Export
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------
    
    content = VGroup( 
                  Item( 'default_perspective~' ),
                  label       = 'Description',
                  show_border = True
              )
    
#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_children ( self ):
        """ Returns the unadapted extension points immediately contained within
            this one.
        """
        return self.adaptee.perspectives + self.adaptee.views
        
    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'default_perspective' ]
    
#-------------------------------------------------------------------------------
#  'ViewAdapter' class:
#-------------------------------------------------------------------------------

class ViewAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:    
    #---------------------------------------------------------------------------
    
    name       = Export
    id         = Export
    class_name = Export
    image      = Export
    position   = Export
    visible    = Export
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------
    
    content = VGroup( 
                  Item( 'name~' ),
                  Item( 'id~' ),
                  Item( 'class_name~' ),
                  Item( 'image~' ),
                  Item( 'position~' ),
                  Item( 'visible~', width = -40 ),
                  label       = 'Description',
                  show_border = True
              )
    
#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'name', 'id', 'class_name', 'image', 'position', 'visible' ]
    
#-------------------------------------------------------------------------------
#  'PerspectiveAdapter' class:
#-------------------------------------------------------------------------------

class PerspectiveAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:    
    #---------------------------------------------------------------------------
    
    name             = Export
    id               = Export
    class_name       = Export
    editor_area_size = Export
    show_editor_area = Export
    enabled          = Export
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------
    
    content = VGroup( 
                  Item( 'name~' ),
                  Item( 'id~' ),
                  Item( 'class_name~' ),
                  Item( 'editor_area_size~' ),
                  Item( 'show_editor_area~', width = -40 ),
                  Item( 'enabled~',          width = -40 ),
                  label       = 'Description',
                  show_border = True
              )
    
#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_children ( self ):
        """ Returns the unadapted extension points immediately contained within
            this one.
        """
        return self.adaptee.contents
        
    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'id', 'class_name', 'editor_area_size', 'show_editor_area', 
                 'enabled' ]
    
#-------------------------------------------------------------------------------
#  'BrandingAdapter' class:
#-------------------------------------------------------------------------------

class BrandingAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:    
    #---------------------------------------------------------------------------
    
    application_name = Export
    about_additions  = Export
    about_image      = Export
    application_icon = Export
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------
    
    content = VGroup( 
                  Item( 'application_name~' ),
                  Item( 'application_icon~' ),
                  Item( 'about_image~' ),
                  Item( 'about_additions~' ),
                  label       = 'Description',
                  show_border = True
              )
    
#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'application_name', 'application_icon', 'about_image', 
                 '*about_additions' ]

