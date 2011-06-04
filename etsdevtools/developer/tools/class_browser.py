#-------------------------------------------------------------------------------
#
#  Implements a Python class browser 'component' intended to serve as a base
#  for other Python-based tools.
#
#  Written by: David C. Morrill
#
#  Date: 07/01/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import shelve
import pyclbr

from time \
    import time, sleep

from os \
    import listdir, environ, stat

from os.path \
    import join, isdir, exists, splitext, abspath, basename, dirname

from threading \
    import Thread, Lock

from traits.api \
    import HasPrivateTraits, Str, Int, Float, List, Instance, Event, File, \
           Directory, Property, Any, Delegate, true

from traitsui.api \
    import TreeEditor, TreeNode, ObjectTreeNode, TreeNodeObject, UI, View, \
    HGroup, Item

from traitsui.menu \
    import NoButtons

from traits.trait_base \
    import traits_home

from pyface.timer.api \
    import do_later

from enthought.developer.api \
    import FilePosition, PythonFilePosition

#-------------------------------------------------------------------------------
#  Gets a reference to the class browser database:
#-------------------------------------------------------------------------------

def get_cb_db ( mode = 'r' ):
    """ Gets a reference to the class browser database.
    """
    try:
        return shelve.open( join( traits_home(), 'class_browser' ),
                            flag = mode, protocol = -1 )
    except:
        return None

#-------------------------------------------------------------------------------
#  Returns the 'pyclbr' class browser data for a specified file:
#-------------------------------------------------------------------------------

# The lock used to manage access to the class browser data base:
cb_db_lock = Lock()

def get_pyclbr ( file_path, python_path, update_only = False ):
    """ Returns the 'pyclbr' class browser data for a specified file.
    """
    global cb_db_lock

    # Make sure the file path is a str (db doesn't like unicode):
    file_path = str( file_path )

    # Strip any trailing path separators off (just in case):
    if python_path[-1:] in '/\\':
        python_path = python_path[:-1]

    cb_db_lock.acquire()
    try:
        db      = get_cb_db()
        py_stat = stat( file_path )
        if db is not None:
            pyclbr_stat = db.get( file_path )
            if pyclbr_stat is not None:
                if pyclbr_stat.st_mtime >= py_stat.st_mtime:
                    dic = None
                    if not update_only:
                        dic = db[ file_path + '*' ]
                    return dic
            db.close()

        module, ext = splitext( file_path[ len( python_path ) + 1: ] )
        module      = module.replace( '/', '.' ).replace( '\\', '.' )
        dic         = pyclbr.readmodule( module, [ python_path ] )
        db          = get_cb_db( mode = 'c' )
        if db is not None:
            db[ file_path ]       = py_stat
            db[ file_path + '*' ] = dic

        return dic
    finally:
        if db is not None:
            db.close()
        cb_db_lock.release()

#-------------------------------------------------------------------------------
#  'CBTreeNodeObject' class:
#-------------------------------------------------------------------------------

class CBTreeNodeObject ( TreeNodeObject ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Cached result of 'tno_has_children':
    _has_children = Any

    # Cached result of 'tno_get_children':
    _get_children = Any

    #---------------------------------------------------------------------------
    #  Returns whether children of this object are allowed or not:
    #---------------------------------------------------------------------------

    def tno_allows_children ( self, node ):
        """ Returns whether children of this object are allowed or not.
        """
        return True

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
    #  Returns the 'draggable' version of a specified object:
    #---------------------------------------------------------------------------

    def tno_get_drag_object ( self, node ):
        """ Returns the 'draggable' version of a specified object.
        """
        return self.path

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

    def get_children ( self ):
        """ Gets the object's children.
        """
        raise NotImplementedError

    #---------------------------------------------------------------------------
    #  Extracts the Python source code for a specified item:
    #---------------------------------------------------------------------------

    def extract_text ( self, text ):
        """ Extracts the Python source code for a specified item.
        """
        line_number = self.line_number
        lines       = text.split( '\n' )
        indent      = self.indent( lines[ line_number - 1 ] )

        for j in range( line_number, len( lines ) ):
            line = lines[j]
            if (not self.ignore( line )) and (self.indent( line ) <= indent):
                break
        else:
            j = len( lines )

        for j in range( j - 1, line_number - 2, -1 ):
            if not self.ignore( lines[j] ):
                j += 1
                break

        for i in range( line_number - 2, -1, -1 ):
            if not self.ignore( lines[i] ):
                break
        else:
            i = -1

        for i in range( i + 1, line_number ):
            if not self.is_blank( lines[i] ):
                break

        # Save the starting line and number of lines in the extracted text:
        self.line_number = i
        self.lines       = j - i

        # Return the extracted text fragment:
        return '\n'.join( [ line[ indent: ] for line in lines[ i: j ] ] )

    #---------------------------------------------------------------------------
    #  Returns the amount of indenting of a specified line:
    #---------------------------------------------------------------------------

    def indent ( self, line ):
        """ Returns the amount of indenting of a specified line.
        """
        return (len( line ) - len( line.lstrip() ))

    #---------------------------------------------------------------------------
    #  Returns whether or not a specified line should be ignored:
    #---------------------------------------------------------------------------

    def ignore ( self, line ):
        """ Returns whether or not a specified line should be ignored.
        """
        line = line.lstrip()
        return ((len( line ) == 0) or (line.lstrip()[:1] == '#'))

    #---------------------------------------------------------------------------
    #  Returns whether or not a specified line is blank:
    #---------------------------------------------------------------------------

    def is_blank ( self, line ):
        """ Returns whether or not a specified line is blank.
        """
        return (len( line.strip() ) == 0)

#-------------------------------------------------------------------------------
#  'CBMethod' class:
#-------------------------------------------------------------------------------

class CBMethod ( CBTreeNodeObject ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The class containing this method:
    parent = Any

    # The name of the file containing this class:
    path = Property

    # Name of the method:
    name = Str

    # The starting line number of the method within the source file:
    line_number = Int

    # The number of source code lines in the method:
    lines = Int

    # The text of the method:
    text = Property

    # An object associated with this class (HACK):
    object = Delegate( 'parent' )

    # The additional PythonFilePosition information provided by this object:
    file_position_info = Property

    #---------------------------------------------------------------------------
    #  Implementation of the 'path' property:
    #---------------------------------------------------------------------------

    def _get_path ( self ):
        return self.parent.path

    #---------------------------------------------------------------------------
    #  Implementation of the 'text' property:
    #---------------------------------------------------------------------------

    def _get_text ( self ):
        if self._text is None:
            self._text = self.extract_text( self.parent.parent.text )

        return self._text

    def _set_text ( self, value ):
        pass

    #---------------------------------------------------------------------------
    #  Implementation of the 'file_position_info' property:
    #---------------------------------------------------------------------------

    def _get_file_position_info ( self ):
        if self._file_position_info is None:
            self._file_position_info = self.parent.file_position_info.copy()
            self._file_position_info[ 'method_name' ] = self.name

        return self._file_position_info

    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:
    #---------------------------------------------------------------------------

    def has_children ( self ):
        """ Returns whether or not the object has children.
        """
        return False

    #---------------------------------------------------------------------------
    #  Gets the object's children:
    #---------------------------------------------------------------------------

    def get_children ( self ):
        """ Gets the object's children.
        """
        return []

    #---------------------------------------------------------------------------
    #  Returns the 'draggable' version of a specified object:
    #---------------------------------------------------------------------------

    def tno_get_drag_object ( self, node ):
        """ Returns the 'draggable' version of a specified object.
        """
        # Get the text to force 'line_number' to be set correctly:
        self.text

        return PythonFilePosition( name      = self.name,
                                   file_name = self.path,
                                   line      = self.line_number + 1,
                                   lines     = self.lines ).set(
                                   **self.file_position_info )

#-------------------------------------------------------------------------------
#  'CBClass' class:
#-------------------------------------------------------------------------------

class CBClass ( CBTreeNodeObject ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The module containing this class:
    parent = Any

    # The name of the file containing this class:
    path = Property

    # Name of the class:
    name = Str

    # The 'pyclbr' class descriptor:
    descriptor = Any

    # The starting line number of the class within the source file:
    line_number = Int

    # The number of source code lines in the class:
    lines = Int

    # Methods defined on the class:
    methods = List( CBMethod )

    # Should methods be displayed:
    show_methods = Delegate( 'parent' )

    # The text of the class:
    text = Property

    # An object associated with this class (HACK):
    object = Delegate( 'parent' )

    # The additional PythonFilePosition information provided by this object:
    file_position_info = Property

    #---------------------------------------------------------------------------
    #  Implementation of the 'path' property:
    #---------------------------------------------------------------------------

    def _get_path ( self ):
        return self.parent.path

    #---------------------------------------------------------------------------
    #  Implementation of the 'text' property:
    #---------------------------------------------------------------------------

    def _get_text ( self ):
        if self._text is None:
            self._text = self.extract_text( self.parent.text )

        return self._text

    def _set_text ( self ):
        pass

    #---------------------------------------------------------------------------
    #  Implementation of the 'file_position_info' property:
    #---------------------------------------------------------------------------

    def _get_file_position_info ( self ):
        if self._file_position_info is None:
            self._file_position_info = self.parent.file_position_info.copy()
            self._file_position_info[ 'class_name' ] = self.name

        return self._file_position_info

    #---------------------------------------------------------------------------
    #  Handles the 'descriptor' trait being changed:
    #---------------------------------------------------------------------------

    def _descriptor_changed ( self, descriptor ):
        """ Handles the 'descriptor' trait being changed.
        """
        self.line_number = descriptor.lineno

    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:
    #---------------------------------------------------------------------------

    def has_children ( self ):
        """ Returns whether or not the object has children.
        """
        return (self.show_methods and (len( self.descriptor.methods ) > 0))

    #---------------------------------------------------------------------------
    #  Gets the object's children:
    #---------------------------------------------------------------------------

    def get_children ( self ):
        """ Gets the object's children.
        """
        methods = [ CBMethod( parent      = self,
                              name        = name,
                              line_number = line_number )
                    for name, line_number in self.descriptor.methods.items() ]
        methods.sort( lambda l, r: cmp( l.name, r.name ) )
        #self.methods = methods
        return methods

    #---------------------------------------------------------------------------
    #  Returns the 'draggable' version of a specified object:
    #---------------------------------------------------------------------------

    def tno_get_drag_object ( self, node ):
        """ Returns the 'draggable' version of a specified object.
        """
        # Get the text to force 'line_number' to be set correctly:
        self.text

        return PythonFilePosition( name      = self.name,
                                   file_name = self.path,
                                   line      = self.line_number + 1,
                                   lines     = self.lines ).set(
                                   **self.file_position_info )

#-------------------------------------------------------------------------------
#  'CBModule' class:
#-------------------------------------------------------------------------------

class CBModule ( CBTreeNodeObject ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Parent of this module:
    parent = Any

    # Name of file system path to this module:
    path = Property

    # Name of the module:
    name = Str

    # The starting line number of the module:
    line_number = Int( 0 )

    # The number of source code lines in the modules:
    lines = Int( -1 )

    # Classes contained in the module:
    classes = List( CBClass )

    # Should methods be displayed:
    show_methods = Delegate( 'parent' )

    # The text of the module:
    text = Property

    # An object associated with this module:
    object = Any

    # The additional PythonFilePosition information provided by this object:
    file_position_info = Property

    #---------------------------------------------------------------------------
    #  Implementation of the 'path' property:
    #---------------------------------------------------------------------------

    def _get_path ( self ):
        return join( self.parent.path, self.name + '.py' )

    #---------------------------------------------------------------------------
    #  Implementation of the 'text' property:
    #---------------------------------------------------------------------------

    def _get_text ( self ):
        if self._text is None:
            fh = open( self.path, 'rb' )
            self._text = fh.read()
            fh.close()

        return self._text

    def _set_text ( self ):
        pass

    #---------------------------------------------------------------------------
    #  Implementation of the 'file_position_info' property:
    #---------------------------------------------------------------------------

    def _get_file_position_info ( self ):
        if self._file_position_info is None:
            self._file_position_info = self.parent.file_position_info.copy()
            self._file_position_info[ 'module_name' ] = self.name

        return self._file_position_info

    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:
    #---------------------------------------------------------------------------

    def has_children ( self ):
        """ Returns whether or not the object has children.
        """
        dic     = get_pyclbr( self.path, self.parent.cb_path.path )
        path    = abspath( self.path )
        classes = [ CBClass( parent     = self,
                             name       = name,
                             descriptor = descriptor )
                    for name, descriptor in dic.items()
                        if path == abspath( descriptor.file ) ]
        classes.sort( lambda l, r: cmp( l.name, r.name ) )
        self.classes = classes
        return (len( self.classes ) > 0)

    #---------------------------------------------------------------------------
    #  Gets the object's children:
    #---------------------------------------------------------------------------

    def get_children ( self ):
        """ Gets the object's children.
        """
        self.tno_has_children()
        return self.classes

    #---------------------------------------------------------------------------
    #  Returns the 'draggable' version of a specified object:
    #---------------------------------------------------------------------------

    def tno_get_drag_object ( self, node ):
        """ Returns the 'draggable' version of a specified object.
        """
        return PythonFilePosition( file_name = self.path ).set(
                                   **self.file_position_info )

#-------------------------------------------------------------------------------
#  'CBModuleFile' class:
#-------------------------------------------------------------------------------

class CBModuleFile ( CBTreeNodeObject ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Name of file system path to this module:
    path = File

    # The Python path this module is located in:
    python_path = Directory

    # Name of the module:
    name = Property

    # The starting line number of the module:
    line_number = Int( 0 )

    # The number of source code lines in the module:
    lines = Int( -1 )

    # Classes contained in the module:
    classes = List( CBClass )

    # Should methods be displayed:
    show_methods = true

    # The text of the module:
    text = Property

    # An object associated with this module (HACK):
    object = Any

    # The additional PythonFilePosition information provided by this object:
    file_position_info = Property

    #---------------------------------------------------------------------------
    #  Implementation of the 'name' property:
    #---------------------------------------------------------------------------

    def _get_name ( self ):
        return splitext( basename( self.path ) )[0]

    #---------------------------------------------------------------------------
    #  Implementation of the 'text' property:
    #---------------------------------------------------------------------------

    def _get_text ( self ):
        if self._text is None:
            fh = open( self.path, 'rb' )
            self._text = fh.read()
            fh.close()

        return self._text

    def _set_text ( self ):
        pass

    #---------------------------------------------------------------------------
    #  Implementation of the 'file_position_info' property:
    #---------------------------------------------------------------------------

    def _get_file_position_info ( self ):
        if self._file_position_info is None:
            path        = abspath( dirname( self.path ) )
            python_path = abspath( self.python_path )
            self._file_position_info = { 'module_name': self.name,
                                         'package_name':
                 path[ len( python_path ) + 1: ].replace( '/',  '.' ).replace(
                                                          '\\', '.' ) }

        return self._file_position_info

    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:
    #---------------------------------------------------------------------------

    def has_children ( self ):
        """ Returns whether or not the object has children.
        """
        dic     = get_pyclbr( self.path, self.python_path )
        path    = abspath( self.path )
        classes = [ CBClass( parent     = self,
                             name       = name,
                             descriptor = descriptor )
                    for name, descriptor in dic.items()
                        if path == abspath( descriptor.file ) ]
        classes.sort( lambda l, r: cmp( l.name, r.name ) )
        self.classes = classes
        return (len( self.classes ) > 0)

    #---------------------------------------------------------------------------
    #  Gets the object's children:
    #---------------------------------------------------------------------------

    def get_children ( self ):
        """ Gets the object's children.
        """
        self.tno_has_children()
        return self.classes

    #---------------------------------------------------------------------------
    #  Returns the 'draggable' version of a specified object:
    #---------------------------------------------------------------------------

    def tno_get_drag_object ( self, node ):
        """ Returns the 'draggable' version of a specified object.
        """
        return PythonFilePosition( file_name = self.path ).set(
                                   **self.file_position_info )

    #---------------------------------------------------------------------------
    #  Returns the persistent state of the object:
    #---------------------------------------------------------------------------

    def __getstate__ ( self ):
        return self.get( 'path', 'python_path', 'show_methods' )

#-------------------------------------------------------------------------------
#  'CBPackageBase' class:
#-------------------------------------------------------------------------------

class CBPackageBase ( CBTreeNodeObject ):

    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:
    #---------------------------------------------------------------------------

    def has_children ( self ):
        """ Returns whether or not the object has children.
        """
        path = self.path
        for name in listdir( path ):
            cur_path = join( path, name )
            if isdir( cur_path ) and exists( join( cur_path, '__init__.py' ) ):
                return True
            module, ext = splitext( name )
            if ((ext == '.py') and
                CBModule( parent = self, name = module ).tno_has_children()):
                return True
        return False

    #---------------------------------------------------------------------------
    #  Gets the object's children:
    #---------------------------------------------------------------------------

    def get_children ( self ):
        """ Gets the object's children.
        """
        packages = []
        modules  = []
        path     = self.path
        cb_path  = self.cb_path
        for name in listdir( path ):
            cur_path = join( path, name )
            if isdir( cur_path ) and exists( join( cur_path, '__init__.py' ) ):
                packages.append( CBPackage( cb_path = cb_path,
                                            parent  = self,
                                            name    = name ) )
            else:
                module, ext = splitext( name )
                if ext == '.py':
                    modules.append( CBModule( parent = self, name = module ) )
        packages.sort( lambda l, r: cmp( l.name, r.name ) )
        modules.sort(  lambda l, r: cmp( l.name, r.name ) )
        return (packages + modules)

#-------------------------------------------------------------------------------
#  'CBPackage' class:
#-------------------------------------------------------------------------------

class CBPackage ( CBPackageBase ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The Python path this package is part of:
    cb_path = Instance( 'CBPath' )

    # Parent of this package:
    parent = Any

    # Name of file system path to this package:
    path = Property

    # Name of the package:
    name = Str

    # The starting line number of the module:
    line_number = Int( 0 )

    # The number of source code lines in the module:
    lines = Int( -1 )

    # Should methods be displayed:
    show_methods = Delegate( 'parent' )

    # The text of the package (i.e. the '__init__.py' file):
    text = Property

    # An object associated with this package (HACK):
    object = Any

    # The additional PythonFilePosition information provided by this object:
    file_position_info = Property

    #---------------------------------------------------------------------------
    #  Implementation of the 'path' property:
    #---------------------------------------------------------------------------

    def _get_path ( self ):
        return join( self.parent.path, self.name )

    #---------------------------------------------------------------------------
    #  Implementation of the 'text' property:
    #---------------------------------------------------------------------------

    def _get_text ( self ):
        if self._text is None:
            fh = open( join( self.path, '__init__.py' ), 'rb' )
            self._text = fh.read()
            fh.close()

        return self._text

    def _set_text ( self ):
        pass

    #---------------------------------------------------------------------------
    #  Implementation of the 'file_position_info' property:
    #---------------------------------------------------------------------------

    def _get_file_position_info ( self ):
        if self._file_position_info is None:
            path    = abspath( self.path )
            cb_path = abspath( self.cb_path.path )
            self._file_position_info = { 'package_name':
                 path[ len( cb_path ) + 1: ].replace( '/',  '.' ).replace(
                                                      '\\', '.' ) }

        return self._file_position_info

#-------------------------------------------------------------------------------
#  'CBPath' class:
#-------------------------------------------------------------------------------

class CBPath ( CBPackageBase ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The Python path this path represents (i.e. itself):
    cb_path = Property

    # Name of a file system directory used as a Python path:
    path = Str

    # Should methods be displayed:
    show_methods = true

    # The additional PythonFilePosition information provided by this object:
    file_position_info = Property

    #---------------------------------------------------------------------------
    #  The implementation of the 'cb_path' property:
    #---------------------------------------------------------------------------

    def _get_cb_path ( self ):
        return self

    #---------------------------------------------------------------------------
    #  Implementation of the 'file_position_info' property:
    #---------------------------------------------------------------------------

    def _get_file_position_info ( self ):
        if self._file_position_info is None:
            self._file_position_info = {}

        return self._file_position_info

#-------------------------------------------------------------------------------
#  'ClassBrowserPaths' class:
#-------------------------------------------------------------------------------

class ClassBrowserPaths ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # List of all Python source file paths in the name space:
    paths = List( CBPath )

    #---------------------------------------------------------------------------
    #  Handles the 'paths' trait being changed:
    #---------------------------------------------------------------------------

    def _paths_changed ( self, paths ):
        """ Handles the 'paths' trait being changed.
        """
        global module_analyzer

        module_analyzer.add_paths( paths )

#-------------------------------------------------------------------------------
#  'ModuleAnalyzer' class:
#-------------------------------------------------------------------------------

class ModuleAnalyzer ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The interval (in seconds) between successive scans:
    interval = Float( 600.0 )

    # The queue lock:
    lock = Any

    # The work queue:
    queue = List

    # The paths already placed on the queue:
    paths = List( Str )

    # The number of packages processed:
    packages = Int

    # The number of modules processed:
    modules = Int

    # The number of modules analyzed:
    analyzed = Int

    # The number of errors encountered:
    errors = Int

    #---------------------------------------------------------------------------
    #  Adds paths to the work queue:
    #---------------------------------------------------------------------------

    def add_paths ( self, paths ):
        """ Adds paths to the work queue.
        """
        paths = [ cb_path.path for cb_path in paths
                  if cb_path.path not in self.paths ]
        if len( paths ) > 0:
            self.paths.extend( paths )
            if self.lock is None:
                self.lock = Lock()
                do_later( self.start_thread )
            self.init_queue( paths )

    #---------------------------------------------------------------------------
    #  Initializes the work queue:
    #---------------------------------------------------------------------------

    def init_queue ( self, paths ):
        """ Initializes the work queue.
        """
        self.lock.acquire()
        self.packages += len( paths )
        do_path        = self.do_path
        self.queue.extend( [ ( do_path, path, path ) for path in paths ] )
        self.lock.release()

    #---------------------------------------------------------------------------
    #  Starts a background class analysis thread running:
    #---------------------------------------------------------------------------

    def start_thread ( self ):
        """ Starts a background class analysis thread running.
        """
        thread = Thread( target = self.process_queue )
        thread.setDaemon( True )
        thread.start()

    #---------------------------------------------------------------------------
    #  Processes items in the work queue:
    #---------------------------------------------------------------------------

    def process_queue ( self ):
        """ Processes items in the work queue.
        """
        start_time = time()
        while True:
            self.lock.acquire()

            if len( self.queue ) == 0:
                self.lock.release()
                start_time = time()
                while time() < (start_time + self.interval):
                    sleep( 1.0 )
                self.init_queue( self.paths )
                #print ('Analyzed %d out of %d modules in %d directories '
                #       'with %d errors in %.2f seconds' % ( self.analyzed,
                #       self.modules, self.packages, self.errors,
                #       time() - start_time ))
            else:
                item = self.queue.pop()
                try:
                    item[0]( *item[1:] )
                except:
                    #print 'Error processing:', item[1]
                    self.errors += 1

                self.lock.release()

    #---------------------------------------------------------------------------
    #  Processes a Python path:
    #---------------------------------------------------------------------------

    def do_path ( self, path, python_path ):
        """ Processes a Python path.
        """
        do_path   = self.do_path
        do_pyclbr = self.do_pyclbr
        dirs      = []
        files     = []
        for name in listdir( path ):
            cur_path = join( path, name )
            if isdir( cur_path ) and exists( join( cur_path, '__init__.py' ) ):
                self.packages += 1
                dirs.append( ( do_path, cur_path, python_path ) )
            else:
                module, ext = splitext( name )
                if ext == '.py':
                    self.modules += 1
                    files.append( ( do_pyclbr, cur_path, python_path ) )

        self.queue.extend( dirs + files )

    #---------------------------------------------------------------------------
    #  Processes a Python module:
    #---------------------------------------------------------------------------

    def do_pyclbr ( self, cur_path, python_path ):
        """ Processes a Python module.
        """
        if get_pyclbr( cur_path, python_path, True ) is not None:
            self.analyzed += 1

# Create a singleton module analyzer:
module_analyzer = ModuleAnalyzer()

#-------------------------------------------------------------------------------
#  Defines the class browser tree editor(s):
#-------------------------------------------------------------------------------

# Common tree nodes:
cb_tree_nodes = [
    TreeNode(       node_for   = [ ClassBrowserPaths ],
                    auto_open  = True,
                    auto_close = True,
                    children   = 'paths',
                    label      = '=Python Path' ),
    ObjectTreeNode( node_for   = [ CBPath ],
                    label      = 'path',
                    auto_close = True ),
    ObjectTreeNode( node_for   = [ CBPackage ],
                    label      = 'name',
                    auto_close = True,
                    icon_group = 'package',
                    icon_open  = 'package' ),
    ObjectTreeNode( node_for   = [ CBModule, CBModuleFile ],
                    label      = 'name',
                    children   = 'ignore',
                    auto_close = True,
                    icon_group = 'module',
                    icon_open  = 'module' ),
    ObjectTreeNode( node_for   = [ CBClass ],
                    label      = 'name',
                    auto_close = True,
                    icon_group = 'class',
                    icon_open  = 'class' ),
    ObjectTreeNode( node_for   = [ CBMethod ],
                    label      = 'name',
                    icon_group = 'method',
                    icon_open  = 'method' )
]

# Define a tree-only version:
cb_tree_editor = TreeEditor(
    editable = False,
    selected = 'object',
    nodes    = cb_tree_nodes
)

#-------------------------------------------------------------------------------
#  'ClassBrowser' class:
#-------------------------------------------------------------------------------

class ClassBrowser ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Class Browser' )

    # Root of the class browser tree:
    root = Instance( ClassBrowserPaths )

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
        Item( name       = 'root',
              editor     = cb_tree_editor,
              show_label = False
        )
    )

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
            self.file_position = PythonFilePosition(
                                     name      = object.name,
                                     file_name = object.path,
                                     line      = object.line_number + 1,
                                     lines     = object.lines ).set(
                                     **object.file_position_info )

#-------------------------------------------------------------------------------
#  Displays a class browser:
#-------------------------------------------------------------------------------

def class_browser_for ( paths, show_methods = True ):
    """ Displays a class browser.
    """
    if len( paths ) == 0:
        import sys
        paths = sys.path[:]
    paths.sort()
    return ClassBrowser( root  = ClassBrowserPaths(
                         paths = [ CBPath( path         = path,
                                           show_methods = show_methods )
                                   for path in paths ] ) )

#-------------------------------------------------------------------------------
#  Create export objects:
#-------------------------------------------------------------------------------

try:
    paths = environ[ 'PYTHONPATH' ].split( ';' )
except:
    paths = []

class_browser = view = class_browser_for( paths )

