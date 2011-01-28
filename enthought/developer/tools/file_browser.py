#-------------------------------------------------------------------------------
#
#  File browser view.
#
#  Written by: David C. Morrill
#
#  Date: 07/14/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from os \
    import listdir

from os.path \
    import exists, join, isdir, isfile

from enthought.traits.api \
    import HasPrivateTraits, Any, Instance, File, Directory, Str, Property, \
           Callable

from enthought.traits.ui.api \
    import View, Item, TreeEditor, TreeNodeObject, ObjectTreeNode

from enthought.developer.api \
    import FilePosition

#-------------------------------------------------------------------------------
#  'BaseNode' class:
#-------------------------------------------------------------------------------

class BaseNode ( TreeNodeObject ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Path to this node:
    path = Str

    # Name of this node:
    name = Str

    # Complete file name of this node:
    file_name = Property

    #---------------------------------------------------------------------------
    #  Implementation of the 'file_name' property:
    #---------------------------------------------------------------------------

    def _get_file_name ( self ):
        return join( self.path, self.name )

    #---------------------------------------------------------------------------
    #  Returns the 'draggable' version of a specified object:
    #---------------------------------------------------------------------------

    def tno_get_drag_object ( self, node ):
        """ Returns the 'draggable' version of a specified object.
        """
        return self.file_name

#-------------------------------------------------------------------------------
#  'PathNode' class:
#-------------------------------------------------------------------------------

class PathNode ( BaseNode ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Filter used to determine if a specified path is accepted:
    path_filter = Callable

    # Filter used to determine if a specified file is accepted:
    file_filter = Callable

    # Factory used to create new file nodes:
    file_factory = Callable

    #---------------------------------------------------------------------------
    #  Returns whether chidren of this object are allowed or not:
    #---------------------------------------------------------------------------

    def tno_allows_children ( self, node ):
        """ Returns whether chidren of this object are allowed or not.
        """
        return True

    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:
    #---------------------------------------------------------------------------

    def tno_has_children ( self, node = None ):
        """ Returns whether or not the object has children.
        """
        return (len( self.tno_get_children( node ) ) > 0)

    #---------------------------------------------------------------------------
    #  Gets the object's children:
    #---------------------------------------------------------------------------

    def tno_get_children ( self, node ):
        """ Gets the object's children.
        """
        if self._get_children is None:
            paths = []
            files = []
            path  = self.file_name
            path_filter = self.path_filter
            if path_filter is None:
                path_filter = lambda f: 1
            file_filter = self.file_filter
            if file_filter is None:
                file_filter = lambda f: 1
            file_factory = self.file_factory
            if file_factory is None:
                file_factory = lambda p, n: FileNode( path = p, name = n )
            try:
                for name in listdir( path ):
                    new_path = join( path, name )
                    if isdir( new_path ):
                        if path_filter( new_path ):
                            paths.append(
                                PathNode( path        = path,
                                          name        = name,
                                          path_filter = path_filter,
                                          file_filter = file_filter ) )
                    elif isfile( new_path ):
                        if file_filter( new_path ):
                            files.append( file_factory( path, name ) )
            except:
                pass
            paths.sort( lambda l, r: cmp( l.name, r.name ) )
            files.sort( lambda l, r: cmp( l.name, r.name ) )
            self._get_children = paths + files

        return self._get_children

#-------------------------------------------------------------------------------
#  'RootNode' class:
#-------------------------------------------------------------------------------

class RootNode ( PathNode ):

    pass

#-------------------------------------------------------------------------------
#  'FileNode' class:
#-------------------------------------------------------------------------------

class FileNode ( BaseNode ):

    #---------------------------------------------------------------------------
    #  Returns whether chidren of this object are allowed or not:
    #---------------------------------------------------------------------------

    def tno_allows_children ( self, node ):
        """ Returns whether chidren of this object are allowed or not.
        """
        return False

#-------------------------------------------------------------------------------
#  Tree editor definition:
#-------------------------------------------------------------------------------

tree_editor = TreeEditor(
    editable  = False,
    selected  = 'selected',
    nodes     = [
        ObjectTreeNode( node_for   = [ RootNode ],
                        auto_open  = True,
                        label      = 'path' ),
        ObjectTreeNode( node_for   = [ PathNode ],
                        auto_close = True,
                        label      = 'name' ),
        ObjectTreeNode( node_for   = [ FileNode ],
                        label      = 'name' )
    ]
)

#-------------------------------------------------------------------------------
#  'FileBrowser' class:
#-------------------------------------------------------------------------------

class FileBrowser ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'File Browser' )

    # The persistence id for this object:
    id = Str( 'enthought.developer.tools.file_browser.state',
              save_state_id = True )

    # File browser root path:
    root_path = Directory( '/', save_state = True )

    # Root of the class browser tree:
    root = Instance( RootNode, { 'path': r'C:\svnroot' } )

    # The current file position:
    file_position = Instance( FilePosition,
                              connect = 'from: selected file position' )

    # The current file name:
    file_name = File( connect = 'from: selected file' )

    # The current directory:
    directory = Directory( connect = 'from: selected directory' )

    # Current path (file or directory):
    path = File( connect   = 'from: selected path',
                 draggable = 'Drag the selected path.' )

    # The current selected node:
    selected = Any

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( name       = 'root',
              editor     = tree_editor,
              show_label = False
        )
    )

    options = View(
        Item( 'root_path',
              label = 'Root Path',
              width = 300
        ),
        title   = 'File Browser Options',
        id      = 'enthought.developer.tools.file_browser.options',
        buttons = [ 'OK', 'Cancel' ]
    )

    #---------------------------------------------------------------------------
    #  Handles the 'root_path' trait being changed:
    #---------------------------------------------------------------------------

    def _root_path_changed ( self, path ):
        """ Handles the 'path' trait being changed.
        """
        if exists( path ):
            self.root = RootNode( path = path )

    #---------------------------------------------------------------------------
    #  Handles a path/file being selected:
    #---------------------------------------------------------------------------

    def _selected_changed ( self, selected ):
        """ Handles a path/file being selected.
        """
        if isinstance( selected, PathNode ):
            self.directory = selected.file_name
        else:
            self.file_name     = selected.file_name
            self.file_position = FilePosition( file_name = selected.file_name )
        self.path = selected.file_name

#-------------------------------------------------------------------------------
#  Create export objects:
#-------------------------------------------------------------------------------

view = FileBrowser()

