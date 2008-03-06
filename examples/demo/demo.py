#-------------------------------------------------------------------------------
#  
#  A Traits UI demo that borrows heavily from the design of the wxPython demo.  
#  
#  Written by: David C. Morrill
#  
#  Date: 09/15/2005
#  
#  (c) Copyright 2005 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:  
#-------------------------------------------------------------------------------

import sys

from enthought.traits.api \
    import HasTraits, HasPrivateTraits, Str, List, Instance, Property, Any, \
           Code, HTML, true, false
           
from enthought.traits.ui.api \
    import TreeEditor, ObjectTreeNode, TreeNodeObject, View, Item, VSplit, \
           Tabbed, VGroup, HGroup, Heading, Handler, UIInfo, InstanceEditor, \
           Include, spring

from string \
    import uppercase, lowercase
    
from os \
    import listdir
    
from os.path \
    import join, isdir, split, splitext, dirname, abspath
    
#-------------------------------------------------------------------------------
#  Global data:  
#-------------------------------------------------------------------------------
        
# Define the code used to populate the 'execfile' dictionary:
exec_str =  """from enthought.traits.api import *

"""
    
#----------------------------------------------------------------------------
#  Return a 'user-friendly' name for a specified string:
#----------------------------------------------------------------------------

def user_name_for ( name ):
    name = name.replace( '_', ' ' )
    return name[:1].upper() + name[1:]

#-------------------------------------------------------------------------------
#  Parses the contents of a specified source file into module comment and 
#  source text:  
#-------------------------------------------------------------------------------

def parse_source ( file_name ):
    try:
        fh     = open( file_name, 'rb' )
        source = fh.read().strip()
        fh.close()
    
        # Extract out the module comment as the description:
        comment = ''
        quotes  = source[:3]
        if (quotes == '"""') or (quotes == "'''"):
            col = source.find( quotes, 3 )
            if col >= 0:
                comment = source[ 3: col ]
                source  = source[ col + 3: ].strip()
                
        return ( comment, source )
        
    except:
        return ( '', '' )
    
#-------------------------------------------------------------------------------
#  'DemoFileHandler' class:  
#-------------------------------------------------------------------------------
        
class DemoFileHandler ( Handler ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
        
    # The current 'info' object (for use by the 'write' method):
    info = Instance( UIInfo )
    
    #---------------------------------------------------------------------------
    #  Initializes the view:  
    #---------------------------------------------------------------------------
        
    def init ( self, info ):
        # Save the reference to the current 'info' object:
        self.info = info 
        
        # Set up the 'print' logger:
        df         = info.object
        df.log     = ''
        sys.stdout = sys.stderr = self
        
        # Read in the demo source file:
        df.description, df.source = parse_source( df.path )
        
        # Try to run the demo source file:
        locals = df.parent.init_dic
        locals[ '__name__' ] = '___main___'
        sys.modules[ '__main__' ].__file__ = df.path
        try:
            execfile( df.path, locals, locals )
            demo = self._get_object( 'modal_popup', locals )
            if demo is not None:
                demo = ModalDemoButton( demo = demo )
            else:
                demo = self._get_object( 'popup', locals )
                if demo is not None:
                    demo = DemoButton( demo = demo )
                else:    
                    demo = self._get_object( 'demo', locals )
        except Exception, excp:
            demo = DemoError( msg = str( excp ) )
            
        df.demo = demo
  
    #---------------------------------------------------------------------------
    #  Closes the view:
    #---------------------------------------------------------------------------
    
    def closed ( self, info, is_ok ):
        """ Closes the view.
        """
        info.object.demo = None
         
    #---------------------------------------------------------------------------
    #  Get a specified object from the execution dictionary:  
    #---------------------------------------------------------------------------
    
    def _get_object ( self, name, dic ):
        object = dic.get( name ) or dic.get( name.capitalize() )
        if object is not None:
            if isinstance( type( object ), type ):
                try:
                    object = object()
                except:
                    pass
                    
            if isinstance( object, HasTraits ):
                return object
                
        return None
                                        
    #---------------------------------------------------------------------------
    #  Handles 'print' output:  
    #---------------------------------------------------------------------------
                              
    def write ( self, text ):
        self.info.object.log += text
        
    def flush ( self ):
        pass
            
# Create a singleton instance:            
demo_file_handler = DemoFileHandler()

#-------------------------------------------------------------------------------
#  'DemoError' class:
#-------------------------------------------------------------------------------

class DemoError ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
    
    # The error message text:
    msg = Code
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------
    
    traits_view = View(
        VGroup(
            Heading( 'Error in source file' ), 
            Item( 'msg', style = 'custom', show_label = False ),
        )
    )
                        
#-------------------------------------------------------------------------------
#  'DemoButton' class:  
#-------------------------------------------------------------------------------
                      
class DemoButton ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
    
    # The demo to be launched via a button:
    demo = Instance( HasTraits )
    
    # The demo view item to use:
    demo_item = Item( 'demo',
        show_label = False,
        editor     = InstanceEditor( label = 'Run demo...', kind = 'live' )
    )
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------
        
    traits_view = View(
        VGroup(
            VGroup( 
                Heading( 'Click the button to run the demo:' ),
                '20' 
            ),
            HGroup( 
                spring,
                Include( 'demo_item' ),
                spring
            )
        ),
        resizable = True
    ) 
                        
#-------------------------------------------------------------------------------
#  'ModalDemoButton' class:  
#-------------------------------------------------------------------------------
                      
class ModalDemoButton ( DemoButton ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
    
    # The demo view item to use:
    demo_item = Item( 'demo',
        show_label = False,
        editor     = InstanceEditor( label = 'Run demo...', kind = 'modal' )
    )
     
#-------------------------------------------------------------------------------
#  'DemoTreeNodeObject' class:  
#-------------------------------------------------------------------------------
        
class DemoTreeNodeObject ( TreeNodeObject ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
        
    # Cached result of 'tno_has_children':
    _has_children = Any
    
    # Cached result of 'tno_get_children':
    _get_children = Any

    #---------------------------------------------------------------------------
    #  Returns whether chidren of this object are allowed or not:  
    #---------------------------------------------------------------------------

    def tno_allows_children ( self, node ):
        """ Returns whether chidren of this object are allowed or not.
        """
        return self.allows_children
    
    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:  
    #---------------------------------------------------------------------------

    def tno_has_children ( self, node = None ):
        """ Returns whether or not the object has children.
        """
        if self._has_children is None:
            self._has_children = self.has_children()
            
        return self._has_children
        
    #---------------------------------------------------------------------------
    #  Gets the object's children:  
    #---------------------------------------------------------------------------

    def tno_get_children ( self, node ):
        """ Gets the object's children.
        """
        if self._get_children is None:
            self._get_children = self.get_children()
            
        return self._get_children
        
    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:  
    #---------------------------------------------------------------------------

    def has_children ( self, node ):
        """ Returns whether or not the object has children.
        """
        raise NotImplementedError
        
    #---------------------------------------------------------------------------
    #  Gets the object's children:  
    #---------------------------------------------------------------------------

    def get_children ( self, node ):
        """ Gets the object's children.
        """
        raise NotImplementedError
    
#-------------------------------------------------------------------------------
#  'DemoFile' class:  
#-------------------------------------------------------------------------------
        
class DemoFile ( DemoTreeNodeObject ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
    
    # Parent of this file:
    parent = Any
    
    # Name of file system path to this file:
    path = Property
    
    # Name of the file:
    name = Str
    
    # UI form of the 'name':
    nice_name = Property
    
    # Files don't allow children:
    allows_children = false
    
    # Description of what the demo does:
    description = HTML
    
    # Source code for the demo:
    source = Code
    
    # Demo object whose traits UI is to be displayed:
    demo = Instance( HasTraits )
    
    # Log of all print messages displayed:
    log = Code
    
    #---------------------------------------------------------------------------
    #  Implementation of the 'path' property:  
    #---------------------------------------------------------------------------
        
    def _get_path ( self ):
        return join( self.parent.path, self.name + '.py' )
        
    #---------------------------------------------------------------------------
    #  Implementation of the 'nice_name' property:  
    #---------------------------------------------------------------------------
                
    def _get_nice_name ( self ):
        return user_name_for( self.name )
        
    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:  
    #---------------------------------------------------------------------------

    def has_children ( self ):
        """ Returns whether or not the object has children.
        """
        return False
    
#-------------------------------------------------------------------------------
#  'DemoPath' class:  
#-------------------------------------------------------------------------------
        
class DemoPath ( DemoTreeNodeObject ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
     
    # Parent of this package:
    parent = Any
    
    # Name of file system path to this package:
    path = Property
    
    # Name of the directory:
    name = Str
    
    # UI form of the 'name':
    nice_name = Property
    
    # Description of the contents of the directory:
    description = Property( HTML )
    
    # Source code contained in the '__init__.py' file:
    source = Property( Code )
    
    # Dictionary containing symbols defined by the path's '__init__.py' file:
    init_dic = Property
    
    # Should .py files be included?    
    use_files = true
    
    # Paths do allow children:
    allows_children = true
    
    #---------------------------------------------------------------------------
    #  Implementation of the 'path' property:  
    #---------------------------------------------------------------------------
        
    def _get_path ( self ):
        return join( self.parent.path, self.name )
        
    #---------------------------------------------------------------------------
    #  Implementation of the 'nice_name' property:  
    #---------------------------------------------------------------------------
                
    def _get_nice_name ( self ):
        return user_name_for( self.name )
        
    #---------------------------------------------------------------------------
    #  Implementation of the 'description' property:  
    #---------------------------------------------------------------------------
                
    def _get_description ( self ):
        if self._description is None:
            self._get_init()
            
        return self._description
        
    #---------------------------------------------------------------------------
    #  Implementation of the 'source' property:  
    #---------------------------------------------------------------------------
                
    def _get_source ( self ):
        if self._source is None:
            self._get_init()
            
        return self._source
        
    #---------------------------------------------------------------------------
    #  Implementation of the 'init_dic' property:  
    #---------------------------------------------------------------------------
                
    def _get_init_dic ( self ):
        init_dic = {}
        description, source = parse_source( join( self.path, '__init__.py' ) )
        exec (exec_str + source) in init_dic
        
        return init_dic
        
        # fixme: The following code should work, but doesn't, so we use the
        #        preceding code instead. Changing any trait in the object in
        #        this method causes the tree to behave as if the DemoPath object
        #        had been selected instead of a DemoFile object. May be due to
        #        an 'anytrait' listener in the TreeEditor?
        #if self._init_dic is None:
        #   self._init_dic = {}
        #   #exec self.source in self._init_dic
        #return self._init_dic.copy()
        
    #---------------------------------------------------------------------------
    #  Initializes the description and source from the path's '__init__.py' 
    #  file:  
    #---------------------------------------------------------------------------

    def _get_init ( self ):      
        if self.use_files:
            # Read in the '__init__.py' source file (if any):
            self._description, source = parse_source( 
                                              join( self.path, '__init__.py' ) )
        else:
            self._description = ('<img src="traits_ui_demo.jpg">')
            source = ''
            
        self._source = exec_str + source 
        
    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:  
    #---------------------------------------------------------------------------

    def has_children ( self ):
        """ Returns whether or not the object has children.
        """
        path = self.path
        for name in listdir( path ):
            cur_path = join( path, name )
            if isdir( cur_path ):
                return True
                
            if self.use_files:
                name, ext = splitext( name )
                if (ext == '.py') and (name != '__init__'):
                    return True
                    
        return False
        
    #---------------------------------------------------------------------------
    #  Gets the object's children:  
    #---------------------------------------------------------------------------

    def get_children ( self ):
        """ Gets the object's children.
        """
        dirs  = []
        files = []
        path  = self.path
        for name in listdir( path ):
            cur_path = join( path, name )
            if isdir( cur_path ):
                if self.has_py_files( cur_path ):
                    dirs.append( DemoPath( parent = self, name = name ) )
                    
            elif self.use_files:
                name, ext = splitext( name )
                if (ext == '.py') and (name != '__init__'):
                    files.append( DemoFile( parent = self, name = name ) )
                    
        dirs.sort(  lambda l, r: cmp( l.name, r.name ) )
        files.sort( lambda l, r: cmp( l.name, r.name ) )
        
        return (dirs + files)
        
    #---------------------------------------------------------------------------
    #  Returns whether the specified path contains any .py files:  
    #---------------------------------------------------------------------------
    
    def has_py_files ( self, path ):
        for name in listdir( path ):
            cur_path = join( path, name )
            if isdir( cur_path ):
                if self.has_py_files( cur_path ):
                    return True
                    
            else:
                name, ext = splitext( name )
                if ext == '.py':
                    return True
                    
        return False
    
#-------------------------------------------------------------------------------
#  Defines the demo tree editor:  
#-------------------------------------------------------------------------------

path_view = View( 
    Tabbed( 
        Item( 'description', 
              label      = 'Description',
              show_label = False,
              style      = 'readonly'
        ),
        Item( 'source',
              label      = 'Source',
              show_label = False,
              style      = 'custom'
        ),
        export = 'DockWindowShell',
        id     = 'tabbed'
    ),
    id      = 'enthought.traits.ui.demos.demo.path_view',
    dock    = 'horizontal'
)

demo_view = View( 
     VSplit( 
         Tabbed( 
             Item( 'description',
                   label      = 'Description',
                   show_label = False,
                   style      = 'readonly'
             ),
             Item( 'source',
                   label      = 'Source',
                   show_label = False,
                   style      = 'custom'
             ),
             Item( 'demo',
                   label      = 'Demo',
                   show_label = False,
                   style      = 'custom',
                   resizable  = True
             ),
             export = 'DockWindowShell'
         ),
         VGroup(
             Item( 'log',
                   show_label = False,
                   style      = 'readonly'
             ),
             label = 'Log'
         ),
         export = 'DockWindowShell',
         id     = 'vsplit'
     ),
     id      = 'enthought.traits.ui.demos.demo.file_view',
     dock    = 'horizontal',
     handler = demo_file_handler
)
                   
demo_tree_editor = TreeEditor(
    nodes = [
        ObjectTreeNode( node_for = [ DemoPath ],
                        label    = 'nice_name',
                        view     = path_view ),
        ObjectTreeNode( node_for = [ DemoFile ],
                        label    = 'nice_name',
                        view     = demo_view )
    ]
)
    
#-------------------------------------------------------------------------------
#  'Demo' class:  
#-------------------------------------------------------------------------------
        
class Demo ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------

    # Path to the root demo directory:
    path = Str
    
    # Root path object for locating demo files:
    root = Instance( DemoPath )
        
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------
        
    traits_view = View( 
        Item( name       = 'root',
              id         = 'root',
              show_label = False,
              editor     = demo_tree_editor
        ),
        title     = 'Traits UI Demo',
        id        = 'enthought.traits.ui.demos.demo.Demo',
        dock      = 'horizontal',
        resizable = True,
        width     = 950,
        height    = 600
    )
                        
    #---------------------------------------------------------------------------
    #  Handles the 'root' trait being changed:  
    #---------------------------------------------------------------------------
    
    def _root_changed ( self, root ):
        """ Handles the 'root' trait being changed.
        """
        root.parent = self
    
#-------------------------------------------------------------------------------
#  Run the demo:
#-------------------------------------------------------------------------------
        
if __name__ == '__main__':
    import sys
    
    path, name = split( dirname( abspath( sys.argv[0] ) ) )
    Demo( path = path, 
          root = DemoPath( name = name, use_files = False )
    ).configure_traits() 
    
