#-------------------------------------------------------------------------------
#
#  File Space plugin
#
#  Written by: David C. Morrill
#
#  Date: 06/27/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from os \
    import listdir, remove, rmdir, mkdir, rename, access, W_OK

from os.path \
    import join, isfile, isdir, basename, dirname, splitext

from enthought.traits.api \
    import HasPrivateTraits, Instance, Property, Int, Str, Any, Regex, List, \
           File, Directory, Callable, true, false, Bool

from enthought.traits.ui.api \
    import View, Item, TreeEditor, TreeNode, TreeNodeObject, ObjectTreeNode

from enthought.pyface.api \
    import error, confirm, YES
    
from enthought.developer.api \
    import FilePosition

#-------------------------------------------------------------------------------
#  'FileSpaceBaseNode' class:
#-------------------------------------------------------------------------------

class FileSpaceBaseNode ( TreeNodeObject ):

    #---------------------------------------------------------------------------
    #  Returns whether chidren of this object are allowed or not:  
    #---------------------------------------------------------------------------

    def tno_allows_children ( self, node ):
        """ Returns whether chidren of this object are allowed or not.
        """
        return True

    #---------------------------------------------------------------------------
    #  Returns whether a specified path should be included in the file space:
    #---------------------------------------------------------------------------

    def include ( self, path, level = 0 ):
        """ Returns whether a specified path should be included in the file
            space.
        """
        filter        = self.file_space.filter
        no_filter     = (filter is None)
        extensions    = self.file_space.extensions
        no_extensions = (len( extensions ) == 0)
        dirs          = []
        
        for file in listdir( path ):
            fn = join( path, file )
            if isfile( fn ):
                base, extension = splitext( fn )
                if ((no_filter and no_extensions) or
                    (extension in extensions) or
                    ((not no_filter) and filter( fn ))):
                    return True
            elif isdir( fn ):
                dirs.append( fn )
                
        level += 1
        if level < self.file_space.levels:
            for dir in dirs:
                if self.include( dir, level ):
                    return True
                    
        return False
        
    #---------------------------------------------------------------------------
    #  Returns whether a specified file is included in the file space:  
    #---------------------------------------------------------------------------
    
    def include_file ( self, fn ):
        """ Returns whether a specified file is included in the file space.
        """
        file_space      = self.file_space
        base, extension = splitext( fn )
        return (((file_space.filter is None) and 
                  len( file_space.extensions == 0)) or
                (extension in file_space.extensions) or
                ((file_space.filter is not None) and file_space.filter( fn )))

#-------------------------------------------------------------------------------
#  'FileSpaceNode' class:
#-------------------------------------------------------------------------------

class FileSpaceNode ( FileSpaceBaseNode ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The valid file space roots:
    roots = List # ( FileSpaceRootNode )
    
    # The file space filter function:
    filter = Callable
    
    # The list of legal file extensions:
    extensions = List( Str )
    
    # The number of levels to search for valid files:
    levels = Int( 3 )
           
    #---------------------------------------------------------------------------
    #  Returns the persistent state of the object:  
    #---------------------------------------------------------------------------

    def __getstate__ ( self ):
        return self.get( 'roots', 'extensions', 'levels' )
    
    #---------------------------------------------------------------------------
    #  Handles the 'roots' trait being changed:  
    #---------------------------------------------------------------------------
    
    def _roots_changed ( self, roots ):
        """ Handles the 'roots' trait being changed.
        """
        for root in roots:
            root.file_space = self
            
    def _roots_items_changed ( self, event ):
        """ Handles the 'roots' trait being changed.
        """
        for root in event.added:
            root.file_space = self

#-------------------------------------------------------------------------------
#  'FileSpaceRootNode' class:
#-------------------------------------------------------------------------------

class FileSpaceRootNode ( FileSpaceBaseNode ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The root FileSpaceNode:
    file_space = Instance( FileSpaceNode )

    # The file path associated with this node:
    path = Directory

    # The name of the node:
    name = Str

    # The child nodes of this node:
    children = List

    # Has the node been completely initialized yet?
    initialized = false

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View( 
               Item( 'path', width = -300 ),
               Item( 'name' ),
               buttons = [ 'OK', 'Cancel' ],
               title   = 'New File Space Root',
               id = 'enthought.developer.tools.file_space.FileSpaceRootNode'
           )
           
    #---------------------------------------------------------------------------
    #  Returns the persistent state of the object:  
    #---------------------------------------------------------------------------

    def __getstate__ ( self ):
        return self.get( 'path', 'name', 'file_space' )

    #---------------------------------------------------------------------------
    #  Handles changes to the 'children' trait:
    #---------------------------------------------------------------------------

    def _children_items_changed ( self, event ):
        """ Handles changes to the 'children' trait.
        """
        for child in event.added:
            if not isinstance( child, DirectoryNode ):
                continue

            new_path = join( self.path, child.dir_name )
            if isfile( new_path ):
                error( self.handler.parent, 
                       ("Cannot create the directory '%s'.\nThere is already a "
                        "file with that name.") % child.dir_name )
                return

            if not isdir( new_path ):
                try:
                    mkdir( new_path )
                except:
                    error( self.handler.parent, ("An error occurred creating "
                           "the directory '%s'") % child.dir_name )
                    return

            child.set( path = new_path, file_space = self.file_space )

            self.initialized = False

    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:
    #---------------------------------------------------------------------------

    def tno_has_children ( self, node ):
        """ Returns whether or not the object has children.
        """
        self.tno_get_children( node )

        return (len( self.children ) > 0)

    #---------------------------------------------------------------------------
    #  Gets the object's children:
    #---------------------------------------------------------------------------

    def tno_get_children ( self, node ):
        """ Gets the object's children.
        """
        if not self.initialized:
            self.initialized = True
            
            path          = self.path
            file_space    = self.file_space
            filter        = file_space.filter
            no_filter     = (filter is None)
            extensions    = file_space.extensions
            no_extensions = (len( extensions ) == 0)
            files         = []
            dirs          = []
            
            if isdir( path ):
                for file in listdir( path ):
                    fn = join( path, file )
                    if isfile( fn ):
                        base, extension = splitext( fn )
                        if ((no_filter and no_extensions) or
                            (extension in extensions) or
                            ((not no_filter) and filter( fn ))):
                            files.append( FileNode( path       = fn,
                                                    file_space = file_space ) )
                    elif isdir( fn ) and self.include( fn ):
                        dirs.append( DirectoryNode( path       = fn,
                                                    file_space = file_space ) )

            # Sort the directories and files separately:
            dirs.sort(  lambda l, r: cmp( l.name, r.name ) )
            files.sort( lambda l, r: cmp( l.name, r.name ) )

            # Returns the combined list of objects:
            self.children = dirs + files

        return self.children

    #---------------------------------------------------------------------------
    #  Gets the label to display for a specified object:
    #---------------------------------------------------------------------------

    def tno_get_label ( self, node ):
        """ Gets the label to display for a specified object.
        """
        if self.name != '':
            return self.name
            
        return self.path

    #---------------------------------------------------------------------------
    #  Sets the label for a specified node:
    #---------------------------------------------------------------------------

    def tno_set_label ( self, node, label ):        
        """ Sets the label for a specified object.
        """
        self.name = label

    #---------------------------------------------------------------------------
    #  Returns whether or not the object's children can be renamed:
    #---------------------------------------------------------------------------

    def tno_can_rename ( self, node ):
        """ Returns whether or not the object's children can be renamed.
        """
        return access( self.path, W_OK )

    #---------------------------------------------------------------------------
    #  Returns whether or not the object's children can be deleted:
    #---------------------------------------------------------------------------

    def tno_can_delete ( self, node ):
        """ Returns whether or not the object's children can be deleted.
        """
        return access( self.path, W_OK )

    #---------------------------------------------------------------------------
    #  Confirms that a specified object can be deleted or not:
    #  Result = True:  Delete object with no further prompting
    #         = False: Do not delete object
    #         = other: Take default action (may prompt user to confirm delete)
    #---------------------------------------------------------------------------

    def tno_confirm_delete ( self, node = None ):
        """ Confirms that a specified object can be deleted or not.
        """
        return (confirm( self.handler.parent,
               "Delete '%s' from the file space?\n\nNote: No files will be "
               "deleted." % self.root.name,
               'Delete File Space Root' ) == YES)

    #---------------------------------------------------------------------------
    #  Deletes a child at a specified index from the object's children:  
    #---------------------------------------------------------------------------

    def tno_delete_child ( self, node, index ):
        """ Deletes a child at a specified index from the object's children.
        """
        # fixme: This doesn't work right for a cut/paste operation, since it
        # will delete the object, then try to paste the now non-existent 
        # file/directory somewhere else...
        self.children[ index ].delete()
        del self.children[ index ]

    #---------------------------------------------------------------------------
    #  Appends a child to the object's children:  
    #---------------------------------------------------------------------------

    def tno_append_child ( self, node, child ):
        """ Appends a child to the object's children.
        """
        super( FileSpaceRootNode, self ).tno_append_child( node, child )
        self.tno_get_children( node )

    #---------------------------------------------------------------------------
    #  Returns the list of classes that can be added to the object:
    #---------------------------------------------------------------------------

    def tno_get_add ( self, node ):
        """ Returns the list of classes that can be added to the object.
        """
        if access( self.path, W_OK ):
            return [ ( DirectoryNode, True ) ]

        return []
        
    #---------------------------------------------------------------------------
    #  Returns the 'draggable' version of a specified object:  
    #---------------------------------------------------------------------------
                
    def tno_get_drag_object ( self, node ):
        """ Returns the 'draggable' version of a specified object.
        """
        return self.path

#-------------------------------------------------------------------------------
#  'DirectoryNode' class:
#-------------------------------------------------------------------------------

class DirectoryNode ( FileSpaceRootNode ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The user specified name of the directory:
    dir_name = Regex( 'New Folder', r'[A-Za-z.#@$%-_~]+' )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View( 'dir_name{Name}',
                 title   = 'Create New Folder',
                 buttons = [ 'OK', 'Cancel' ],
                 width   = 300 )

    #---------------------------------------------------------------------------
    #  Gets the label to display for a specified object:
    #---------------------------------------------------------------------------

    def tno_get_label ( self, node ):
        """ Gets the label to display for a specified object.
        """
        return basename( self.path )

    #---------------------------------------------------------------------------
    #  Sets the label for a specified node:
    #---------------------------------------------------------------------------

    def tno_set_label ( self, node, label ):        
        """ Sets the label for a specified object.
        """
        old_name = self.path
        dir_name = dirname( old_name )
        new_name = join( dir_name, label )
        try:
            rename( old_name, new_name )
            self.path = new_name
        except:
            error( self.handler.parent, ("An error occurred while trying to "
                   "rename '%s' to '%s'") % ( basename( old_name ), label ) )

    #---------------------------------------------------------------------------
    #  Confirms that a specified object can be deleted or not:
    #  Result = True:  Delete object with no further prompting
    #         = False: Do not delete object
    #         = other: Take default action (may prompt user to confirm delete)
    #---------------------------------------------------------------------------

    def tno_confirm_delete ( self, node = None ):
        """ Confirms that a specified object can be deleted or not.
        """
        return (confirm( self.handler.parent,
                    "Delete '%s' and all of its contents?" % self.name,
                    'Delete Directory' ) == YES)

    #---------------------------------------------------------------------------
    #  Deletes the associated directory from the file system:
    #---------------------------------------------------------------------------

    def delete ( self, path = None ):
        """ Deletes the associated directory from the file system.
        """
        if path is None:
            path = self.path

        not_deleted = 0
        try:
            for name in listdir( path ):
                fn = join( path, name )
                if isfile( fn ):
                    if self.include_file( fn ):
                        remove( fn )
                    else:
                        not_deleted += 1
                elif isdir( fn ) and (not self.delete( fn )):
                    not_deleted += 1
            if not_deleted == 0: 
                rmdir( path )
                return True
        except:
            error( self.handler.parent, "Could not delete '%s'" % fn )

        # Indicate that the directory was not deleted:                       
        return False

#-------------------------------------------------------------------------------
#  'FileNode' class:
#-------------------------------------------------------------------------------

class FileNode ( TreeNodeObject ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The FileSpaceRoot this is a node for:
    file_space = Instance( FileSpaceNode )

    # The path to the associated file:
    path = Str
    
    # The name of the file (no directory):
    name = Property

    #---------------------------------------------------------------------------
    #  Gets the label to display for a specified object:
    #---------------------------------------------------------------------------

    def tno_get_label ( self, node ):
        """ Gets the label to display for a specified object.
        """
        return basename( self.path )

    #---------------------------------------------------------------------------
    #  Sets the label for a specified node:
    #---------------------------------------------------------------------------

    def tno_set_label ( self, node, label ):        
        """ Sets the label for a specified object.
        """
        old_name = self.path
        dir_name = dirname( old_name )
        new_name = join( dir_name, label )
        try:
            rename( old_name, new_name )
            self.path     = new_name
        except:
            error( self.handler.parent, ("An error occurred while trying to "
                   "rename '%s' to '%s'") % ( basename( old_name ), label ) )

    #---------------------------------------------------------------------------
    #  Confirms that a specified object can be deleted or not:
    #  Result = True:  Delete object with no further prompting
    #         = False: Do not delete object
    #         = other: Take default action (may prompt user to confirm delete)
    #---------------------------------------------------------------------------

    def tno_confirm_delete ( self, node = None ):
        """ Confirms that a specified object can be deleted or not.
        """
        return (confirm( self.handler.parent, "Delete '%s'" % self.name,
                         'Delete File' ) == YES)
        
    #---------------------------------------------------------------------------
    #  Returns the 'draggable' version of a specified object:  
    #---------------------------------------------------------------------------
                
    def tno_get_drag_object ( self, node ):
        """ Returns the 'draggable' version of a specified object.
        """
        return self.path

    #---------------------------------------------------------------------------
    #  Deletes the associated file from the file system:
    #---------------------------------------------------------------------------

    def delete ( self ):
        """ Deletes the associated file from the file system.
        """
        try:
            remove( self.path )
        except:
            error( self.handler.parent, "Could not delete the file '%s'" %
                                        basename( self.path )[0] )
                                        
    #---------------------------------------------------------------------------
    #  Implementation of the 'name' property:  
    #---------------------------------------------------------------------------

    def _get_name ( self ):
        return basename( self.path )

#-------------------------------------------------------------------------------
#  File Space tree editor:
#-------------------------------------------------------------------------------

file_space_tree_editor = TreeEditor(
    selected   = 'selected',
    editable   = False,
    lines_mode = 'on',
    nodes      = [ TreeNode(
                       node_for  = [ FileSpaceNode ],
                       label     = '=File Space',
                       children  = 'roots',
                       auto_open = True,
                       add       = [ ( FileSpaceRootNode, True ) ] ),
                   ObjectTreeNode(
                       node_for   = [ DirectoryNode ],
                       children   = 'children',
                       name       = 'Folder',
                       auto_close = True ),
                   ObjectTreeNode(
                       node_for   = [ FileSpaceRootNode ],
                       children   = 'children', 
                       name       = 'File Space Root',
                       auto_close = True ),
                   ObjectTreeNode(
                       node_for = [ FileNode ] ) ]
)
                             
#-------------------------------------------------------------------------------
#  'FileSpace' class:
#-------------------------------------------------------------------------------

class FileSpace ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'File Space' )
    
    # The persistence id for this object:
    id = Str( 'enthought.developer.tools.file_space.state',
              save_state_id = True )
    
    # The root file space node:
    root = Instance( FileSpaceNode, { 'extensions': [ '.py' ] },
                     save_state = True )
    
    # Fake trait to force state save:
    update = Bool( save_state = True )
    
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

    view = View( 
        Item( 'root', 
              show_label = False,
              editor     = file_space_tree_editor
        ),
        title     = 'File Space',
        resizable = True
    )
    
    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------
    
    def __init__ ( self, **traits ):
        """ Initializes the object.
        """
        super( FileSpace, self ).__init__( **traits )
        self._root_changed( None, self.root )
        
#-- Event Handlers -------------------------------------------------------------

    #---------------------------------------------------------------------------
    #  Handles the 'root' trait being changed:  
    #---------------------------------------------------------------------------

    def _root_changed ( self, old, new ):
        """ Handles the 'root' trait being changed.
        """
        self._set_listener( old, True )
        self._set_listener( new, False )
        
    def _set_listener ( self, object, remove ):
        if object is not None:
            object.on_trait_change( self.save_state, remove = remove ) 
            
    #---------------------------------------------------------------------------
    #  Handles the 'selected' trait being changed:  
    #---------------------------------------------------------------------------

    def _selected_changed ( self, selected ):
        """ Handles the 'selected' trait being changed.
        """
        if isinstance( selected, FileNode ):
            self.file_name     = self.path = selected.path
            self.file_position = FilePosition( file_name = selected.path )
        elif isinstance( selected, FileSpaceRootNode ):
            self.directory = self.path = selected.path
            
    #---------------------------------------------------------------------------
    #  Forces the current state to be saved:
    #---------------------------------------------------------------------------

    def save_state ( self ):
        """ Forces the current state to be saved.
        """
        self.update = not self.update
        
    
#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

file_space = view = FileSpace() 

