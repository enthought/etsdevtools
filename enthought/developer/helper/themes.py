#-------------------------------------------------------------------------------
#  
#  Themes for use in creating developer tools.
#  
#  Written by: David C. Morrill
#  
#  Date: 07/25/2007
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import Constant, Delegate, Instance
    
from enthought.traits.ui.api \
    import Item, Theme
    
from enthought.traits.ui.wx.themed_text_editor \
    import ThemedTextEditor
    
from enthought.traits.ui.wx.themed_button_editor \
    import ThemedButtonEditor    
    
#-------------------------------------------------------------------------------
#  Themes:
#-------------------------------------------------------------------------------

# An item that displays the tool title or information:
class TTitle ( Item ):
    show_label = Constant( False )
    style      = Constant( 'readonly' )
    editor     = ThemedTextEditor()
    item_theme = Constant( Theme( '@GB5', content = ( 8, 0 ) ) )

# A standard themed button:    
class TButton ( Item ):
    show_label = Constant( False )
    label      = Delegate( 'editor', modify = True )
    image      = Delegate( 'editor', modify = True )
    editor     = Instance( ThemedButtonEditor, {
                     'theme':       Theme( '@GG5' ),
                     'down_theme':  Theme( '@GE5' ),
                     'hover_theme': Theme( '@GG6' ) } )

# A standard themed text editor:
class TText ( Item ):
    editor = ThemedTextEditor( theme = Theme( '@G04', content = 0 ) )
    
# A theme for displaying a group of items with a group title:    
GroupTitle = Theme( 'gbox', content = ( 3, -1 ) )
    
# A label theme:
LabelTheme = Theme( '@images:GL5', label     = ( -3, 10 ), 
                                   content   = ( 0, -5 ), 
                                   alignment = 'center' )

# An inset label theme:
InsetTheme = Theme( '@ui:inset_grey', content   = -6,
                                      label     = ( 6, 6, 9, 0 ),
                                      alignment = 'center', )


