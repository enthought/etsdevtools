#-------------------------------------------------------------------------------
#
#  Class browser for the user's 'favorite' (most recently used) Python modules.
#
#  Written by: David C. Morrill
#
#  Date: 07/11/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import sys

from os.path \
    import exists, abspath, join

from enthought.traits.api \
    import HasPrivateTraits, Event, List, Range, Instance, Bool, Str, Any

from enthought.traits.ui.api \
    import View, Item, TreeNode, TreeEditor

from enthought.developer.tools.class_browser \
    import CBModuleFile, cb_tree_nodes

from enthought.developer.api \
    import FilePosition

#-------------------------------------------------------------------------------
#  'FavoritesList' class:
#-------------------------------------------------------------------------------

class FavoritesList ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The list of favorite Python source files:
    favorites = List( CBModuleFile )

#-------------------------------------------------------------------------------
#  Favorites tree editor definition:
#-------------------------------------------------------------------------------

favorites_tree_editor = TreeEditor(
    editable = False,
    selected = 'object',
    nodes    = [ TreeNode( node_for  = [ FavoritesList ],
                           auto_open = True,
                           children  = 'favorites',
                           label     = '=Favorites' ) ] + cb_tree_nodes
)

#-------------------------------------------------------------------------------
#  'FavoritesBrowser' class:
#-------------------------------------------------------------------------------

class FavoritesBrowser ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Favorites Browser' )

    # The persistent id used for saving the favorites data:
    id = Str( 'enthought.developer.tools.favorites_browser.state',
              save_state_id = True )

    # Maximum number of favorites to remember:
    max_favorites = Range( 1, 50, 10, save_state = True, mode = 'spinner' )

    # Fake option to force a save:
    update = Bool( save_state = True )

    # The list of favorite Python source files:
    root = Instance( FavoritesList, (), save_state = True )

    # The name of a file to add to the favorites list:
    file_name = Event( droppable = 'Drop a favorite Python source file here.' )

    # Currently selected object node:
    object = Any

    # The currently selected file position:
    file_position = Instance( FilePosition,
                        draggable = 'Drag currently selected file position.',
                        connect   = 'from:file position' )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( 'root',
              editor     = favorites_tree_editor,
              show_label = False
        )
    )

    options = View(
        Item( 'max_favorites',
              label = 'Maximum number of favorites'
        ),
        title   = 'Favorites Browser Options',
        id      = 'enthought.developer.tools.favorites_browser.options',
        buttons = [ 'OK', 'Cancel' ]
    )

    #---------------------------------------------------------------------------
    #  Handles the 'file_name' trait being changed:
    #---------------------------------------------------------------------------

    def _file_name_changed ( self, file_name ):
        """ Handles the 'file_name' trait being changed.
        """
        if exists( file_name ):
            file_name = abspath( str( file_name ) )
            for path in sys.path:
                path = join( abspath( path ), '' )
                if path == file_name[ : len( path ) ]:
                    root = self.root
                    for mf in root.favorites:
                        if file_name == mf.path:
                            break
                    else:
                        root.favorites = ([ CBModuleFile(
                                              path        = file_name,
                                              python_path = path ) ] +
                                          root.favorites)[: self.max_favorites ]
                        self.update = not self.update
                    return

    #---------------------------------------------------------------------------
    #  Handles the 'max_favorites' trait being changed:
    #---------------------------------------------------------------------------

    def _max_favorites_changed ( self, max_favorites ):
        """ Handles the 'max_favorites' trait being changed.
        """
        self.root.favorites = self.root.favorites[ : max_favorites ]
        self.update = not self.update

    #---------------------------------------------------------------------------
    #  Handles the 'object' trait being changed:
    #---------------------------------------------------------------------------

    def _object_changed ( self, object ):
        """ Handles a tree node being selected.
        """
        # If the selected object has a starting line number, then set up
        # the file position for the text fragment the object corresponds to:
        if hasattr( object, 'line_number' ):

            # Read the object's text to force it to calculate the starting
            # line number of number of lines in the text fragment:
            ignore = object.text

            # Set the file position for the object:
            self.file_position = FilePosition(
                                     name      = object.name,
                                     file_name = object.path,
                                     line      = object.line_number + 1,
                                     lines     = object.lines )

#-------------------------------------------------------------------------------
#  Create export objects:
#-------------------------------------------------------------------------------

view = FavoritesBrowser()

