#-------------------------------------------------------------------------------
#  
#  A feature-enabled tool for browsing collections of images.
#  
#  Written by: David C. Morrill
#  
#  Date: 11/10/2007
#  
#  (c) Copyright 2007 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------

""" A feature-enabled tool for browsing collections of images.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasPrivateTraits, Property, Str, List
    
from enthought.traits.ui.api \
    import View, Item
    
from enthought.traits.ui.ui_traits \
    import Image, ATheme
    
from enthought.traits.ui.theme \
    import Theme
    
from enthought.traits.ui.wx.extra.image_editor \
    import ImageEditor
    
from enthought.traits.ui.wx.extra.list_canvas_editor \
    import ListCanvasEditor, ListCanvasAdapter
    
#-------------------------------------------------------------------------------
#  The ListCanvasEditor definition:
#-------------------------------------------------------------------------------

class ImageBrowserAdapter ( ListCanvasAdapter ):
    
    # Disable minimizing all items (to save screen real estate):
    can_minimize = False
    
    ImageItem_theme_active    = ATheme( Theme( 'photo_frame_active',   
                       label  = ( 0, 0, -3, 2 ), content = 0, 
                       border = ( 1, 7, 1, 7 ),
                       alignment = 'center' ) )
    ImageItem_theme_inactive  = ATheme( Theme( 'photo_frame_inactive',
                       label  = ( 0, 0, -3, 2 ), content = 0,
                       border = ( 1, 7, 1, 7 ),
                       alignment = 'center' ) )
    ImageItem_theme_hover     = ATheme( Theme( 'photo_frame_hover',
                       label  = ( 0, 0, -3, 2 ), content = 0,
                       border = ( 1, 7, 1, 7 ),
                       alignment = 'center' ) )
    ImageItem_title          = Property
    ImageItem_tooltip        = Property
    
    def _get_ImageItem_title ( self ):
        return self.item.name
    
    def _get_ImageItem_tooltip ( self ):
        return self.item.name
    
list_canvas_editor = ListCanvasEditor(
    adapter    = ImageBrowserAdapter(),
    scrollable = True,
    operations = [ 'move', 'size', 'status' ]
)

#-------------------------------------------------------------------------------
#  'ImageItem' class:
#-------------------------------------------------------------------------------

class ImageItem ( HasPrivateTraits ):
    
    # The name of the item being displayed:
    name = Str
    
    # The image being displayed:
    image = Image
    
    #-- Traits UI View Definitions ---------------------------------------------
    
    view = View(
        Item( 'image',
              show_label = False,
              editor     = ImageEditor()
        )
    )
    
#-------------------------------------------------------------------------------
#  'ImageBrowser' class:
#-------------------------------------------------------------------------------

class ImageBrowser ( HasPrivateTraits ):
    
    # The name of the tool:
    name = Str( 'Image Browser' )
    
    # The list of image names being browsed:
    image_names = List( Str, connect = 'to: list of image names to browse' )
    
    # The list of ImageItems being browsed:
    images = List( ImageItem )
    
    #-- Traits UI View Definitions ---------------------------------------------
    
    view = View(
        Item( 'images',
              show_label = False,
              editor     = list_canvas_editor
        ),
        title     = 'Image Browser',
        id        = 'enthought.developer.tools.image_browser.ImageBrowser',
        width     = 0.5,
        height    = 0.5,
        resizable = True
    )
    
    #-- Trait Event Handlers ---------------------------------------------------
    
    def _image_names_changed ( self ):
        """ Handles the 'image_names' trait being changed.
        """
        self.images = [ ImageItem( name = image_name, image = image_name )
                        for image_name in self.image_names ]
    
