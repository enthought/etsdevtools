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
    import Item, Theme, TitleEditor, ButtonEditor
    
#-------------------------------------------------------------------------------
#  Themes:
#-------------------------------------------------------------------------------

# An item that displays the tool title or information:
class TTitle ( Item ):
    show_label = Constant( False )
    editor     = TitleEditor()

# A standard themed button:    
class TButton ( Item ):
    show_label = Constant( False )
    editor     = Instance( ButtonEditor, () )
    image      = Delegate( 'editor', modify = True )
    
# A label theme:
LabelTheme = Theme( '@std:GL5', label     = ( -3, 10 ), 
                                content   = ( 0, -5 ), 
                                alignment = 'center' )

# An inset label theme:
InsetTheme = Theme( '@std:inset_grey', content   = -6,
                                       label     = ( 6, 6, 9, 0 ),
                                       alignment = 'center', )


