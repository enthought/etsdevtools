#-------------------------------------------------------------------------------
#  
#  A feature-enabled tool for editing the information associated with images
#  stored in the Traits image library.
#  
#  Written by: David C. Morrill
#  
#  Date: 12/01/2007
#  
#  (c) Copright 2007 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------

""" A feature-enabled tool for editing the information associated with images
    stored in the Traits image library.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------
    
from enthought.traits.ui.api \
    import View, HGroup, VGroup, HSplit, Item, Label, Theme, ListStrEditor
    
from enthought.developer.helper.image_library_editor \
    import ImageLibraryEditor, ImageLibraryItem
 
from enthought.developer.helper.themes \
    import InsetTheme
   
#-------------------------------------------------------------------------------
#  'ImageInfoItem' class:
#-------------------------------------------------------------------------------

class ImageInfoItem ( ImageLibraryItem ):
    """ Represents an ImageInfo object whose information is being edited by an
        ImageInfoEditor.
    """
    
    #-- Traits View Definitions ------------------------------------------------
    
    view = View(
        VGroup(
            VGroup(
                HGroup( Item( 'name',     springy = True ),
                        Item( 'category', springy = True ),
                        group_theme = InsetTheme ),
                VGroup( 
                    Item( 'description', style = 'custom' ),
                    group_theme = InsetTheme
                ),
                VGroup(
                    Item( 'copyright',
                          label = '   Copyright',
                          style = 'custom' ),
                    group_theme = InsetTheme
                ),
                group_theme = '@std:GL5',
            ),
            VGroup(
                HSplit(
                    VGroup(
                        Label( 'Keywords', InsetTheme ),
                        Item( 'keywords', 
                              editor = ListStrEditor( auto_add = True ) ),
                        group_theme = '@std:XG1',
                        show_labels = False,
                    ),
                    VGroup(
                        Label( 'License', InsetTheme ),
                        Item( 'license', style = 'custom' ),
                        group_theme = '@std:XG1',
                        show_labels = False,
                    ),
                    id = 'splitter'
                ),
                group_theme = '@std:GL5',
            ),
            group_theme = '@std:XG0',
        ),
        id = 'enthought.developer.tools.image_info_editor.ImageInfoItem'
    )
    
#-------------------------------------------------------------------------------
#  'ImageInfoEditor' class:
#-------------------------------------------------------------------------------    

class ImageInfoEditor ( ImageLibraryEditor ):
    """ Allows a user to edit the information associated with ImageInfo objects
        whose corresponding image names are passed to it.
    """
    
    #-- Overridden ImageLibraryEditor Class Constants --------------------------
    
    # The label/title of the editor for use in the view:
    editor_title = 'Image Information Editor'
    
    # The persistence id for the image library editor:
    editor_id = 'enthought.developer.tools.image_info_editor.ImageInfoEditor'
                 
    # Editor item factory class:
    item_class = ImageInfoItem
        
#-------------------------------------------------------------------------------
#  Test Code:
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    ImageInfoEditor( image_names = [ 
        '@std:BlackChromeT', '@std:BlackChromeB', '@std:notebook_open',
        '@std:notebook_close'
    ] ).configure_traits()
    
