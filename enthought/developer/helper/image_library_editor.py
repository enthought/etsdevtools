#-------------------------------------------------------------------------------
#  
#  Defines base classes for creating Traits UI Image Library editors.
#  
#  Written by: David C. Morrill
#  
#  Date: 12/01/2007
#  
#  (c) Copright 2007 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------

""" Defines base classes for creating Traits UI Image Library editors.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasPrivateTraits, Instance, Str, List, Property, Constant, \
           on_trait_change
    
from enthought.traits.ui.api \
    import View, HSplit, Item, ListEditor
    
from enthought.traits.ui.image.image \
    import ImageLibrary, ImageInfo
    
from enthought.developer.helper.library_manager \
    import LibraryManager
   
#-------------------------------------------------------------------------------
#  'ImageLibraryItem' class:
#-------------------------------------------------------------------------------

class ImageLibraryItem ( HasPrivateTraits ):
    """ Represents an ImageInfo object whose information is being edited by 
        some kind of Image Library editor.
    """
    
    # The ImageInfo object being edited:
    image = Instance( ImageInfo )
    
    # The name of the image whose theme is being edited:
    name = Property( depends_on = 'image' )
    
    #-- Property Implementations -----------------------------------------------
    
    def _get_name ( self ):
        return self.image.image_name

    #-- HasTraits Class Overrides ----------------------------------------------

    def trait_context ( self ):
        """ Returns the default context to use for editing or configuring 
            traits.
        """
        return { 'object': self.image }
    
#-------------------------------------------------------------------------------
#  'ImageLibraryEditor' class:
#-------------------------------------------------------------------------------    

class ImageLibraryEditor ( HasPrivateTraits ):
    """ Base class for creating an Image Library Editor.
    """
    
    # The names of the images currently being edited:
    image_names = List( Str, connect = 'to: list of image names to edit' )
    
    # The list of ImageLibraryItem objects currently being edited:
    items = List( ImageLibraryItem )
    
    # The LibraryManager being used to keep track of modified images:
    library = Constant( LibraryManager )
    
    #-- Overridable Class Constants --------------------------------------------
    
    # The label/title of the editor for use in the view:
    editor_title = 'Image Library Editor'
    
    # The persistence id for the image library editor:
    editor_id = ('enthought.developer.tools.image_library_editor.'
                 'ImageLibraryEditor')
                 
    # Editor item factory class:
    item_class = ImageLibraryItem
    
    #-- Traits View Definitions ------------------------------------------------
    
    view = View(
        HSplit(
            Item( 'library',
                  show_label = False,
                  label      = 'Library Manager',
                  style      = 'custom',
                  dock       = 'horizontal',
                  item_theme = '@ui:GL5TB'
            ),
            Item( 'items',
                  id         = 'items',
                  show_label = False,
                  label      = editor_title,
                  style      = 'custom',
                  dock       = 'horizontal',
                  editor     = ListEditor( use_notebook = True,
                                           deletable    = True,
                                           page_name    = '.name',
                                           export       = 'DockWindowShell',
                                           dock_style   = 'tab' )
            ),
            group_theme = '@images:XG0',
            id          = 'splitter'
        ),
        id        = editor_id,
        title     = editor_title,
        width     = 0.7,
        height    = 0.5,
        resizable = True
    )
    
    #-- Traits Event Handlers --------------------------------------------------
    
    @on_trait_change( 'image_names[]' )
    def _image_names_modified ( self, object, name, removed, added ):
        """ Handles image names being added to or removed from the editor.
        """
        items = self.items
        
        # fixme: Remove this code if the problem in the TableEditor that allows
        # the same item to be in both the 'removed' and 'added' list is fixed:
        for name in [ name for name in removed if name in added ]:
            removed.remove( name )
            added.remove(   name )
                        
        for image_name in added:
            item = self._find( image_name )
            if item is None:
                image = ImageLibrary.image_info( image_name )
                if image is not None:
                    items.append( self.item_class( image = image ) )
                
        for image_name in removed:
            item = self._find( image_name )
            if item is not None:
                items.remove( item )
        
    @on_trait_change( 'items[]' )
    def _items_modified ( self, object, name, removed, added ):
        """ Handles the 'items' list being modified.
        """
        library = self.library
            
        for item in removed:
            library.remove( item.image )
        
        for item in added:
            library.add( item.image )

    #-- Private Methods --------------------------------------------------------
    
    def _find ( self, image_name ):
        """ Tries the find a current ImageLibraryItem matching the specified
            **image_name** and return it. Returns None if not found.
        """
        image = ImageLibrary.image_info( image_name )
        if image is not None:
            for item in self.items:
                if image is item.image:
                    return item
                
        return None
    
