#-------------------------------------------------------------------------------
#  
#  A feature-enabled tool for editing themes stored in the Traits image library.
#  
#  Written by: David C. Morrill
#  
#  Date: 11/28/2007
#  
#  (c) Copright 2007 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------

""" A feature-enabled tool for editing themes stored in the Traits image 
    library.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------
    
from enthought.traits.ui.api \
    import View, Item
    
from enthought.developer.editors.theme_editor \
    import ThemeEditor
    
from enthought.developer.helper.image_library_editor \
    import ImageLibraryEditor, ImageLibraryItem
   
#-------------------------------------------------------------------------------
#  'ImageThemeItem' class:
#-------------------------------------------------------------------------------

class ImageThemeItem ( ImageLibraryItem ):
    """ Represents an ImageInfo object whose Theme is being edited by an
        ImageThemeEditor.
    """
    
    #-- Traits View Definitions ------------------------------------------------
    
    view = View(
        Item( 'theme',
              show_label = False,
              editor     = ThemeEditor()
        )
    )
    
#-------------------------------------------------------------------------------
#  'ImageThemeEditor' class:
#-------------------------------------------------------------------------------    

class ImageThemeEditor ( ImageLibraryEditor ):
    """ Allows a user to edit the Theme associated with ImageInfo objects
        whose corresponding image names are passed to it.
    """
    
    #-- Overridden ImageLibraryEditor Class Constants --------------------------
    
    # The label/title of the editor for use in the view:
    editor_title = 'Image Theme Editor'
    
    # The persistence id for the image library editor:
    editor_id = 'enthought.developer.tools.image_theme_editor.ImageThemeEditor'
                 
    # Editor item factory class:
    item_class = ImageThemeItem
        
#-------------------------------------------------------------------------------
#  Test Code:
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    ImageThemeEditor( image_names = [ 
        '@std:BlackChromeT', '@std:BlackChromeB', '@std:notebook_open',
        '@std:notebook_close'
    ] ).configure_traits()
    
