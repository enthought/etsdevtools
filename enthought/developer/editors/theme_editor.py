#-------------------------------------------------------------------------------
#
#  A custom editor for Theme instances.
#
#  Written by: David C. Morrill
#
#  Date: 11/27/2007
#
#  (c) Copyright 2007 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

""" A custom editor for Theme instances.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasTraits, Str, Int, List, Enum, Bool, Any, Property

from enthought.traits.ui.api \
    import View, HGroup, VGroup, Item, Label, Theme, NullEditor, \
           ListStrEditor, spring

from enthought.traits.ui.basic_editor_factory \
    import BasicEditorFactory

from enthought.traits.ui.wx.ui_editor \
    import UIEditor

from enthought.developer.helper.themes \
    import LabelTheme

from list_canvas_editor \
    import ListCanvasEditor, ListCanvasAdapter

from margin_editor \
    import MarginEditor

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# The margin editor being used:
margin_editor = MarginEditor()

#-------------------------------------------------------------------------------
#  The ListCanvasEditor definition:
#-------------------------------------------------------------------------------

class ThemeEditorAdapter ( ListCanvasAdapter ):

    # The editor this adapter is working on behalf of:
    editor = Any

    # Disable minimizing all items:
    can_minimize = False

    # Make sure the list canvas item reacts to all theme changes made by the
    # editor:
    mutable_theme = True

    # The themes to use for list canvas items:
    theme_active   = Property
    theme_inactive = Property
    theme_hover    = Property

    # The titles to display for the various test items:
    Person_title       = Str( 'A Test Person' )
    ShoppingList_title = Str( 'A Shopping List' )
    ALabel_title       = Str( 'A Label' )
    title              = Str

    # Turn debugging on for the Debug instance:
    Debug_debug = Bool( True )

    def _get_theme_active ( self ):
        return self.editor.value

    def _get_theme_inactive ( self ):
        return self.editor.value

    def _get_theme_hover ( self ):
        return self.editor.value

#-------------------------------------------------------------------------------
#  Test classes for use with the ListCanvasEditor:
#-------------------------------------------------------------------------------

class BasePerson ( HasTraits ):

    name   = Str
    age    = Int
    gender = Enum( 'Male', 'Female' )

    view = View(
        VGroup( 'name', 'age', 'gender' )
    )

base_person = BasePerson()

class Person ( BasePerson ):

    pass

person = Person()

default_shopping_list = [
    'Carrots',
    'Potatoes (5 lb. bag)',
    'Cocoa Puffs',
    'Ice Cream (French Vanilla)',
    'Peanut Butter',
    'Whole wheat bread',
    'Ground beef (2 lbs.)',
    'Paper towels',
    'Soup (3 cans)',
    'Laundry detergent'
]

class BaseShoppingList ( HasTraits ):

    shopping_list = List( Str, default_shopping_list )

    view = View(
        Item( 'shopping_list',
              show_label = False,
              width      = 160,
              height     = 130,
              padding    = -4,
              editor     = ListStrEditor( title    = 'Shopping List',
                                          auto_add = True )
        )
    )

base_shopping_list = BaseShoppingList()

class ShoppingList ( BaseShoppingList ):

    pass

shopping_list = ShoppingList()

class ALabel ( HasTraits ):

    empty = Str

    view = View(
        Item( 'empty',
              show_label = False,
              width      = -1,
              height     = -1,
              editor     = NullEditor()
        )
    )

label = ALabel()

class Debug ( HasTraits ):

    empty = Str

    view = View(
        Item( 'empty',
              show_label = False,
              width      = 100,
              height     = 100,
              editor     = NullEditor()
        )
    )

debug = Debug()

#-------------------------------------------------------------------------------
#  '_ThemeEditor' class:
#-------------------------------------------------------------------------------

class _ThemeEditor ( UIEditor ):
    """ A custom editor for Theme instances.
    """

    # Indicate that the editor is resizable. This value overrides the default.
    scrollable = True

    # The display mode for the sample editor items:
    mode = Enum( 'Label and content', 'Label only', 'Content only' )

    # The list of items the test theme is editing using a ListCanvasEditor:
    items = List( [ debug, person, shopping_list ] )

    #-- HasTraits Class Method Overrides ---------------------------------------

    def init_ui ( self, parent ):
        """ Creates the traits UI for the editor.
        """
        return self.edit_traits( context = { 'object': self.value,
                                             'editor': self },
                                 parent  = parent )

    def traits_view ( self ):
        """ Returns the default traits view for the object's class.
        """
        return View(
            VGroup(
                HGroup(
                    VGroup(
                        Label( 'Content', LabelTheme ),
                        Item( 'content', editor = margin_editor ),
                        show_labels = False
                    ),
                    VGroup(
                        Label( 'Label', LabelTheme ),
                        Item( 'label', editor = margin_editor ),
                        show_labels = False
                    ),
                    VGroup(
                        Label( 'Border', LabelTheme ),
                        Item( 'border', editor = margin_editor ),
                        show_labels = False
                    )
                ),
                HGroup(
                    spring,
                    Item( 'editor.mode' ),
                    '30',
                    Item( 'alignment', style = 'custom' ),
                    spring,
                    group_theme = Theme( '@std:GL5',
                                         content = ( 0, 0, -7, -4 ) )
                ),
                Item( 'editor.items',
                      show_label = False,
                      height     = 270,
                      editor     = ListCanvasEditor(
                                       theme      = '@std:GL5',
                                       adapter    = ThemeEditorAdapter(
                                                        editor = self ),
                                       scrollable = True,
                                       operations = [ 'size' ] )
                ),
                group_theme = '@std:XG0'
            ),
            kind = 'subpanel',
        )

    #-- Trait Event Handlers ---------------------------------------------------

    def _mode_changed ( self, mode ):
        """ Handle the editor sample item's mode being changed.
        """
        if mode == 'Label and content':
            self.items = [ debug, person, shopping_list ]
        elif mode == 'Label only':
            self.items = [ debug, label ]
        else:
            self.items = [ debug, base_person, base_shopping_list ]

#-------------------------------------------------------------------------------
#  Create the editor factory object:
#-------------------------------------------------------------------------------

# Editor factory for Theme objects:
class ThemeEditor ( BasicEditorFactory ):

    # The editor class to be created:
    klass = _ThemeEditor

if __name__ == '__main__':
    from enthought.traits.api import HasTraits, Instance

    class Test ( HasTraits ):
        theme = Instance( Theme, ( '@std:BlackChromeB', ) )

        view = View(
            Item( 'theme',
                  show_label = False,
                  editor     = ThemeEditor()
            ),
            resizable = True
        )

    Test().configure_traits()

