#-------------------------------------------------------------------------------
#  
#  A feature-enabled file sieve tool.
#  
#  Written by: David C. Morrill
#  
#  Date: 10/16/2007
#  
#  (c) Copright 2007 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------

""" A feature-enabled file sieve tool.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from threading \
    import Thread
    
from time \
    import sleep, time, localtime, strftime

from os \
    import walk, stat
    
from os.path \
    import abspath, dirname, basename, splitext, isdir, split, join

from stat \
    import ST_SIZE, ST_MTIME
    
from enthought.traits.api \
    import HasPrivateTraits, Str, Int, Long, Enum, List, Float, Bool, \
           Property, Button, Instance, Directory, TraitType, TraitError, \
           cached_property
           
from enthought.traits.ui.api \
    import View, VSplit, VGroup, HGroup, Item, TableEditor, TitleEditor, \
           DirectoryEditor, Handler, spring
    
from enthought.traits.ui.table_column \
    import ObjectColumn
    
from enthought.traits.ui.table_filter \
    import TableFilter
    
from enthought.traits.ui.helper \
    import commatize

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# How many files need to be processed before adding to files list:
BatchSize = 100

# How long to sleep (in seconds) before rebuilding the file list:
SleepInterval = 600

# Mapping from standard Python-like relation to legal method name version:
RelationMap = {
    '>=': 'ge',
    '>':  'gt',
    '<=': 'le',
    '<':  'lt',
    '=':  'eq',
    '==': 'eq',
    '!=': 'ne' 
}

# Mapping from date units to seconds:
DateMap = {
    's': 1,
    'M': 60,
    'h': 60 * 60,
    'd': 60 * 60 * 24,
    'w': 60 * 60 * 24 * 7,
    'm': 60 * 60 * 24 * 30,
    'y': 60 * 60 * 24 * 365
}

#-------------------------------------------------------------------------------
#  Table editor definitions:
#-------------------------------------------------------------------------------

class PathColumn ( ObjectColumn ):
    
    def get_value ( self, object ):
        result = self.get_raw_value( object )[ object.prefix: ]
        if result != '':
            return result
            
        return '\\'

class DateColumn ( ObjectColumn ):
    
    def get_value ( self, object ):
        return strftime( self.format, 
                         localtime( self.get_raw_value( object ) ) )
    
files_table_editor = TableEditor(
    columns = [
        ObjectColumn( name     = 'root', 
                      label    = 'File Root',
                      width    = 0.20,
                      editable = False ),
        ObjectColumn( name     = 'ext',      
                      label    = 'Ext.',
                      width    = 0.07,
                      editable = False ),
        PathColumn(   name     = 'dir',
                      label    = 'Directory', 
                      width    = 0.49,
                      editable = False ),
        ObjectColumn( name     = 'size',
                      width    = 0.08,
                      editable = False,
                      format_func = commatize,
                      horizontal_alignment = 'right' ),
        DateColumn(   name     = 'date',
                      label    = 'Date/Time',
                      format   = '%m/%d/%y %I:%M %p', 
                      width    = 0.14,
                      editable = False,
                      horizontal_alignment = 'center' ),
    ],
    other_columns = [
        ObjectColumn( name     = 'name', 
                      label    = 'File Name',
                      width    = 0.20,
                      editable = False ),
        PathColumn(   name     = 'path',      
                      width    = 0.40,
                      editable = False ),
        DateColumn(   name     = 'date',
                      label    = 'Date',
                      format   = '%m/%d/%y', 
                      width    = 0.10,
                      editable = False,
                      horizontal_alignment = 'center' ),
        DateColumn(   name     = 'date',
                      label    = 'Time',
                      format   = '%I:%M %p', 
                      width    = 0.10,
                      editable = False,
                      horizontal_alignment = 'center' ),
    ],
    editable           = False,
    auto_size          = False, 
    selection_bg_color = 0xFBD391,
    selection_color    = 'black',
    selection_mode     = 'rows',
    selected           = 'selected',
    filter_name        = 'filter',
    filtered_indices   = 'filtered_indices'
)
        
#-------------------------------------------------------------------------------
#  'Size' trait:  
#-------------------------------------------------------------------------------
        
class Size ( TraitType ):
    
    is_mapped     = True
    default_value = ''
    info_text = "a file size of the form: ['<='|'<'|'>='|'>'|'='|'=='|'!=']ddd"
          
    def value_for ( self, value ):
        if isinstance( value, basestring ):
            value = value.strip()
            if len( value ) == 0:
                return ( 'ignore', 0 )
                
            relation = '<='
            c        = value[0]
            if c in '<>!=':
                relation = c
                value    = value[1:]
                c        = value[0:1]
                if c == '=':
                    relation += c
                    value     = value[1:]
                value = value.lstrip()
                
            relation = RelationMap[ relation ]
                
            try:
                size = int( value )
                if size >= 0:
                   return ( relation, size )
            except:
                pass
            
        raise TraitError
        
    mapped_value = value_for
    
    def post_setattr ( self, object, name, value ):
        object.__dict__[ name + '_' ] = value
        

    def as_ctrait ( self ):
        """ Returns a CTrait corresponding to the trait defined by this class.
        """
        # Tell the C code that the 'post_setattr' method wants the modified
        # value returned by the 'value_for' method:
        return super( Size, self ).as_ctrait().setattr_original_value( True )
        
#-------------------------------------------------------------------------------
#  'Age' trait:  
#-------------------------------------------------------------------------------
        
class Age ( Size ):
    
    info_text = ("a time interval of the form: ['<='|'<'|'>='|'>'|'='|'=='"
                 "|'!=']ddd['s'|'m'|'h'|'d'|'w'|'M'|'y']")
          
    def value_for ( self, value ):
        if isinstance( value, basestring ):
            value = value.strip()
            if len( value ) == 0:
                return ( 'ignore', 0 )
                
            units = value[-1:].lower()
            if units in 'smhdwy':
                if units == 'm':
                    units = value[-1:]
                value = value[:-1].strip()
            else:
                units = 'd'
                
            if (len( value ) == 0) or (value[-1:] not in '0123456789'):
                value += '1'
                
            try:
                relation, time = super( Age, self ).value_for( value )
                return ( relation, time * DateMap[ units ] )
            except:
                pass
            
        raise TraitError
        
#-------------------------------------------------------------------------------
#  'FileFilter' class:
#-------------------------------------------------------------------------------

class FileFilter ( TableFilter ):
    """ Filter for FileSieve files.
    """
    
    # The full file name path:
    path = Str
    
    # The root portion of the file name:
    root = Str
    
    # The extension portion of the file name:
    ext = Str
    
    # The extension matching rule:
    ext_rule = Enum( 'in', 'eq', 'ne', 'not' )
    
    # The actual extension to match:
    ext_match = Str
    
    # The file size:
    size = Size
    
    # How recently was the file updated?
    age = Age
    
    # Should the file be read-only or not?
    mode = Enum( "Don't care", "Read only", "Read/Write" )
    
    #-- Traits View Definitions ------------------------------------------------
    
    traits_view = View(
        HGroup(
            Item( 'root', label = 'Name' ),
            '_',
            Item( 'ext',  label = 'Ext', width = -40 ),
            '_',
            Item( 'path' ),
            '_',
            Item( 'size', width = -60 ),
            '_',
            Item( 'age', width = -60 ),
#            '_',
#            Item( 'mode' ),
        )
    )

    #-- TableFilter Method Overrides -------------------------------------------
    
    def filter ( self, object ):
        """ Returns whether a specified object meets the filter criteria.
        """
        return ((object.path.find( self.path ) >= 0)       and
                (object.root.find( self.root ) >= 0)       and
                self._ext_test(  object.ext )              and
                self._size_test( object.size )             and
                self._age_test(  object.date, object.now ) and
                self._mode_test( object.read_only ))
                
    #-- Event Handlers ---------------------------------------------------------
    
    def _ext_changed ( self, ext ):
        ext = ext.strip()
        if ext[0:1] == '=':
            self.ext_rule = 'eq'
            ext           = ext[1:]
            if ext[0:1] == '=':
                ext = ext[1:]
        elif ext[0:2] == '!=':
            self.ext_rule = 'ne'
            ext           = ext[2:]
        elif ext[0:1] == '!':
            self.ext_rule = 'not'
            ext           = ext[1:]
        else:
            self.ext_rule = 'in'
            
        self.ext_match = ext
                
    #-- Private Methods --------------------------------------------------------
    
    def _ext_test ( self, ext ):
        """ Returns whether a specified file extension passes the ext relation.
        """
        return getattr( self, '_ext_' + self.ext_rule )( ext, self.ext_match )
        
    def _ext_in ( self, ext, match ):
        return (ext.find( match ) >= 0)
        
    def _ext_not ( self, ext, match ):
        return (ext.find( match ) < 0)
        
    def _ext_eq ( self, ext, match ):
        return (ext == match)
        
    def _ext_ne ( self, ext, match ):
        return (ext != match)
        
    def _size_test ( self, size ):
        """ Returns whether a specified file size passes the size relation.
        """
        relation, limit = self.size_
        return getattr( self, '_size_' + relation )( size, limit )
        
    def _size_le ( self, size, limit ):
        return (size <= limit)
        
    def _size_lt ( self, size, limit ):
        return (size < limit)
        
    def _size_ge ( self, size, limit ):
        return (size >= limit)
        
    def _size_gt ( self, size, limit ):
        return (size > limit)
        
    def _size_eq ( self, size, limit ):
        return (size == limit)
        
    def _size_ne ( self, size, limit ):
        return (size != limit)
        
    def _size_ignore ( self, size, limit ):
        return True
        
    def _age_test ( self, date, now ):
        """ Returns whether a specified file date passes the age relation.
        """
        relation, age = self.age_
        return getattr( self, '_age_' + relation )( date, now - age )
        
    def _age_le ( self, date, age ):
        return (date >= age)
        
    def _age_lt ( self, date, age ):
        return (date > age)
        
    def _age_ge ( self, date, age ):
        return (date <= age)
        
    def _age_gt ( self, date, age ):
        return (date < age)
        
    def _age_eq ( self, date, age ):
        return (date == age)
        
    def _age_ne ( self, date, age ):
        return (date != age)
        
    def _age_ignore ( self, date, age ):
        return True
        
    def _mode_test ( self, readonly ):
        """ Returns whether a specified file's readonly state passes the mode
            relation.
        """
        return ((self.mode == "Don't care") or
               ((self.mode == "Read only")  and readonly) or
               ((self.mode == "Read/Write") and (not readonly)))
        
#-------------------------------------------------------------------------------
#  'File' class:  
#-------------------------------------------------------------------------------
                
class File ( HasPrivateTraits ):
    """ Represents a single file in a FileSieve.
    """
    
    # The fully-qualified name of a file:
    path = Str
    
    # The length of the common path prefix:
    prefix = Int
    
    # The file directory:
    dir = Property
    
    # The name of the file minus any directory information:
    name = Property
    
    # The root of the file name (name minus file extension information):
    root = Property
    
    # The file extension:
    ext = Property
    
    # The size of the file:
    size = Long
    
    # The last modified date of the file:
    date = Float
    
    # The time at which this object was created:
    now = Float
    
    # Is the file read-only?
    read_only = Bool
    
    #-- Property Implementations -----------------------------------------------
    
    @cached_property
    def _get_dir ( self ):
        return dirname( self.path )
        
    @cached_property
    def _get_name ( self ):
        return basename( self.path )
    
    @cached_property
    def _get_root ( self ):
        return splitext( self.name )[0]
    
    @cached_property
    def _get_ext ( self ):
        return splitext( self.name )[1][1:]
        
    #-- Event Handlers ---------------------------------------------------------
    
    def _path_changed ( self, path ):
        try:
            info           = stat( path )
            self.size      = info[ ST_SIZE ]
            self.date      = info[ ST_MTIME ]
            self.read_only = False  # fixme: Implement this...
        except:
            pass
        
#-------------------------------------------------------------------------------
#  'FileWorker' class:
#-------------------------------------------------------------------------------

class FileWorker ( HasPrivateTraits ):
    """ Background thread for initializing and maintaining a list of files
        for a specified path.
    """
    
    # The sieve object whose file list we are updating:
    sieve = Instance( 'FileSieve' )
    
    # The path being processed:
    path = Str
    
    # The file extension being processed:
    ext = Str
    
    # Should the thread be aborted?
    abort = Bool( False )

    #-- Event Handlers ---------------------------------------------------------
        
    def _path_changed ( self ):
        thread = Thread( target = self._process )
        thread.setDaemon( True )
        thread.start()
        
    #-- Private Methods --------------------------------------------------------
    
    def _process ( self ):
        """ Process all of the files contained in the specified path.
        """
        path, ext, sieve = self.path, self.ext, self.sieve
        prefix = len( path )
        
        # Delete all current files (if any):
        del sieve.files[:]
            
        # Get the current time stamp:
        now = time()
        
        # Make the initial pass, emitting the file in small batches so that the
        # user gets some immediate feedback:
        files = []
        for dir, dir_names, file_names in walk( path ):
            for file_name in file_names:
                # Exit if the user has aborted us:
                if self.abort:
                    return
                
                # Add the file to the current batch if the extension matches:
                if (ext == '') or (ext == splitext( file_name )[1]):
                    files.append( File( path   = join( dir, file_name ), 
                                        prefix = prefix,
                                        now    = now ) )
                    
                # If we've reached the batch size, add to files to the sieve
                # object, and start a new batch:
                if len( files ) >= BatchSize:
                    sieve.files.extend( files )
                    del files[:]
                    
        # Make sure we emit the last partial batch (may be empty):
        sieve.files.extend( files )
        
        # Continue to rebuild the list periodically as long as the user has not
        # aborted us:
        while not self.abort:
            
            # Sleep for a while:
            for i in range( SleepInterval ):
                sleep( 1 )
                if self.abort:
                    self.sieve = None
                    return
            
            # Get the current time stamp:
            now = time()
            
            # Iterate over the files again, this time just building a single,
            # large list:
            files = []
            for dir, dir_names, file_names in walk( path ):
                for file_name in file_names:
                    # Exit if the user has aborted us:
                    if self.abort:
                        self.sieve = None
                        return
                      
                    # Add the file to the list if the extension matches:
                    if (ext == '') or (ext == splitext( file_name )[1]):
                        files.append( File( path   = join( dir, file_name ),
                                            prefix = prefix,
                                            now    = now ) )
             
            # Finally, send all files to the sieve at once, so that the user
            # just sees a single update:
            self.sieve.files = files
            
#-------------------------------------------------------------------------------
#  'FileSieveHandler' class:
#-------------------------------------------------------------------------------

class FileSieveHandler ( Handler ):
    
    def closed ( self, info, is_ok ):
        """ Handles the FileSieve view being closed.
        """
        fs = info.object
        if fs.worker is not None:
            fs.worker.abort = True
            fs.worker       = None
        del fs.files[:]
        del fs.selected[:]
        del fs.filtered_indices[:]
        
#-------------------------------------------------------------------------------
#  'FileSieve' class:  
#-------------------------------------------------------------------------------
                
class FileSieve ( HasPrivateTraits ):

    # The name of the plugin:
    name = Str( 'File Sieve' )
    
    # The persistence id for this object:
    id = Str( 'enthought.developer.tools.file_sieve.state',
              save_state_id = True )
         
    # The path specifying the files to be listed:
    path = Directory( save_state = True, connect = 'to: path to sieve' )
    
    # Base path (in normalized form):
    base_path = Str
    
    # Extension to match on:
    ext = Str
    
    # The list of files containing in the specified path:
    files = List( File )
    
    # The list of currently selected files:
    selected = List( File )
    
    # The list of selected file names:
    selected_files = Property( depends_on = 'selected',
                               connect    = 'from: selected file names' )
    
    # The filter used to 'sieve' the list of files:
    filter = Instance( FileFilter, () )
    
    # Select all listed files button:
    select_all = Button( 'Select All' )
    
    # The indices of the table items currently passing the table filter:
    filtered_indices = List( Int )
    
    # The list of filtered file names:
    filtered_files = Property( depends_on = 'filtered_indices', 
                               connect    = 'from: filtered file names' )
    
    # The total number of files being displayed:
    num_files = Property( depends_on = 'filtered_indices' )
    
    # The total size of all filtered files:
    size = Property( depends_on = 'filtered_indices' )
    
    # Should subdirectories of the path be included?
    recursive = Bool( True )
    
    # The current file worker thread object we are using:
    worker = Instance( FileWorker )
    
    #-- Traits View Definitions ------------------------------------------------
    
    view = View(
        VSplit(
            Item( 'path',
                  id     = 'path',
                  editor = DirectoryEditor( entries = 10 ),
                  dock   = 'vertical' ),
            HGroup(
                Item( 'filter', show_label = False, style = 'custom' ),
#                '_',
#                Item( 'recursive' ),
                spring,
                '_',
                Item( 'num_files', 
                      label       = 'Files',
                      style       = 'readonly', 
                      format_func = commatize,
                      width       = -40 ),
                '_',
                Item( 'size', 
                      style       = 'readonly', 
                      format_func = commatize,
                      width       = -70 ),
                '_',
                Item( 'select_all',
                      show_label   = False,
                      enabled_when = 'len( files ) > 0'
                ),
                dock = 'vertical'
            ),
            VGroup(
                HGroup(
                    Item( 'base_path',
                          label   = 'Path',
                          editor  = TitleEditor(),
                          springy = True
                    ),
                    '_',
                    Item( 'ext',
                          editor = TitleEditor()
                    )
                ),
                Item( 'files', 
                      id     = 'files',
                      editor = files_table_editor
                ),
                dock        = 'horizontal',
                show_labels = False
            ),
            id = 'splitter',
        ),
        title     = 'File Sieve',
        id        = 'enthought.developer.tools.file_sieve.FileSieve',
        width     = 0.6,
        height    = 0.7,
        resizable = True,
        handler   = FileSieveHandler
    )
    
    #-- Property Implementations -----------------------------------------------
    
    def _get_num_files ( self ):
        return len( self.filtered_indices )
    
    @cached_property
    def _get_size ( self ):
        files = self.files
        return reduce( lambda l, r: l + files[r].size, self.filtered_indices,
                       0L )
                       
    @cached_property
    def _get_selected_files ( self ):
        return [ file.path for file in self.selected ]
        
    @cached_property
    def _get_filtered_files ( self ):
        files = self.files
        return [ files[i].path for i in self.filtered_indices ]
        
    #-- Event Handlers ---------------------------------------------------------
    
    def _path_changed ( self, path ):
        """ Handles the 'path' trait being changed.
        """
        # Make sure the path has been normalized:
        path = abspath( path )
        
        # Determine the correct starting directory and optional file extension
        # to match on:
        ext = ''
        if not isdir( path ):
            path, name = split( path )
            if not isdir( path ):
                del self.files[:]
                return
                
            root, ext = splitext( name )
            
        self.base_path = path
        self.ext       = ext
        
        if self.worker is not None:
            self.worker.abort = True
            
        self.worker = FileWorker( sieve = self, ext = ext ).set( path = path )
        
    def _select_all_changed ( self ):
        """ Handles the 'Select All' button being pressed.
        """
        files         = self.files
        self.selected = [ files[i] for i in self.filtered_indices ]
        
    def _recursive_changed ( self, recursive ):
        """ Handles the 'recursive' trait being changed.
        """
        # fixme: Implement this...
            
#-- Test Code ------------------------------------------------------------------

if __name__ == '__main__':
    sieve = FileSieve(
        #path = r'C:\svnroot\enthought.trunk\enthought.sweet_pickle_2.1' )
        path = r'C:\svnroot\enthought.trunk\enthought.pyface_3.0' )
        
    #from enthought.developer.helper.fbi import use_fbi
    #use_fbi()
    
    sieve.configure_traits()
