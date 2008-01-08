#-------------------------------------------------------------------------------
#  
#  A custom editor for Margin/Border instances.
#  
#  Written by: David C. Morrill
#  
#  Date: 11/27/2007
#  
#  (c) Copyright 2007 by Enthought, Inc.                                      
#  
#-------------------------------------------------------------------------------

""" A custom editor for Margin/Border instances.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.ui.api \
    import View, VGroup, Item   
    
from enthought.traits.ui.api \
    import Theme
    
from enthought.traits.ui.basic_editor_factory \
    import BasicEditorFactory
    
from enthought.traits.ui.wx.ui_editor \
    import UIEditor       
    
from enthought.traits.ui.wx.themed_slider_editor \
    import ThemedSliderEditor
    
#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# The slider editor being used:
slider_editor = ThemedSliderEditor( slider_color = 0x8B9BDB )

#-------------------------------------------------------------------------------
#  '_MarginEditor' class:
#-------------------------------------------------------------------------------

class _MarginEditor ( UIEditor ):
    """ A custom editor for Margin/Border instances.
    """
    
    # Mark the editor as being resizable:
    scrollable = True
    
    #-- Traits View Definitions ------------------------------------------------
    
    view = View(
        VGroup(
            Item( 'left',   editor = slider_editor ),  
            Item( 'right',  editor = slider_editor ),                         
            Item( 'top',    editor = slider_editor ),  
            Item( 'bottom', editor = slider_editor ),  
            group_theme  = '@images:GL5',
            item_theme   = Theme( '@ui:GreyItemInset',
                                  content = ( -6, -6, -7, -2 ) ),       
            label_theme  = Theme( '@ui:BlueLabelInset',
                                  content = ( -6, -4, -7, 0 ),
                                  label   = ( -3, 8 ) )
        ),
        kind = 'subpanel'
    )
                    
#-------------------------------------------------------------------------------
#  Create the editor factory object:
#-------------------------------------------------------------------------------

# Editor factory for Margin/Border objects:
class MarginEditor ( BasicEditorFactory ):
    
    # The editor class to be created:
    klass = _MarginEditor
       
#-------------------------------------------------------------------------------
#  Test Code:
#-------------------------------------------------------------------------------
    
if __name__ == '__main__':
    from enthought.traits.api import HasTraits, Instance 
    from enthought.traits.ui.ui_traits import Margin
    
    class Test ( HasTraits ):
        margin = Instance( Margin, () )
        
        view = View(
            Item( 'margin', 
                  show_label = False,
                  editor     = MarginEditor()
            ),
            resizable = True
        )
        
    Test().configure_traits()
    
