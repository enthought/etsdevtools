#-------------------------------------------------------------------------------
#
#  A tool for perform live text searches of source files.
#
#  Written by: David C. Morrill
#
#  Date: 07/10/2008
#
#  (c) Copright 2008 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

""" A tool for perform live text searches of source files.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from os \
    import walk, getcwd, listdir

from os.path \
    import basename, dirname, splitext, join

from enthought.traits.api \
    import HasTraits, File, Directory, Str, Bool, Int, Enum, Instance, \
           Property, Any, Callable, cached_property, property_depends_on

from enthought.traits.ui.api \
    import View, VGroup, VSplit, HGroup, Item, TableEditor, CodeEditor, \
           TitleEditor, HistoryEditor, DNDEditor

from enthought.traits.ui.table_column \
    import ObjectColumn

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

FileTypes = {
    'Python': [ '.py' ],
    'C':      [ '.c', '.h' ],
    'C++':    [ '.cpp', '.h' ],
    'Java':   [ '.java' ],
    'Ruby':   [ '.rb' ]
}

#-------------------------------------------------------------------------------
#  The Live Search table editor definition:
#-------------------------------------------------------------------------------

class MatchesColumn1 ( ObjectColumn ):

    def get_value ( self, object ):
        n = len( self.get_raw_value( object ) )
        if n == 0:
            return ''

        return str( n )

class MatchesColumn2 ( ObjectColumn ):

    def is_editable ( self, object ):
        return (len( object.matches ) > 0)

class FileColumn ( ObjectColumn ):

    def get_drag_value ( self, object ):
        return object.full_name

table_editor = TableEditor(
    columns = [
        MatchesColumn1( name        = 'matches',
                        label       = '#',
                        editable    = False,
                        width       = 0.05,
                        horizontal_alignment = 'center' ),
        MatchesColumn2( name        = 'matches',
                        width       = 0.35,
                        format_func = lambda x: (x + [ '' ])[0].strip(),
                        editor      = CodeEditor( line =
                                          'object.live_search.selected_match',
                                        selected_line =
                                          'object.live_search.selected_match' ),
                        style       = 'readonly',
                        edit_width  = 0.95,
                        edit_height = 0.33 ),
        FileColumn(     name        = 'base_name',
                        label       = 'Name',
                        width       = 0.30,
                        editable    = False ),
        ObjectColumn(   name        = 'ext_path',
                        label       = 'Path',
                        width       = 0.30,
                        editable    = False ),
    ],
    filter_name        = 'filter',
    auto_size          = False,
    show_toolbar       = False,
    selected           = 'selected',
    selection_color    = 0x000000,
    selection_bg_color = 0xFBD391
)

#-------------------------------------------------------------------------------
#  'FileSearch' class:
#-------------------------------------------------------------------------------

class FileSearch ( HasTraits ):

    # The currenty root directory being searched:
    root = Directory( getcwd(), entries = 10 )

    # Should sub directories be included in the search:
    recursive = Bool( True )

    # The file types to include in the search:
    file_type = Enum( 'Python', 'C', 'C++', 'Java', 'Ruby' )

    # The current search string:
    search = Str

    # Is the search case sensitive?
    case_sensitive = Bool( False )

    # The live search table filter:
    filter = Property # Instance( TableFilter )

    # The current list of source files being searched:
    source_files = Property # List( SourceFile )

    # The currently selected source file:
    selected = Any # Instance( SourceFile )

    # The contents of the currently selected source file:
    selected_contents = Property # List( Str )

    # The currently selected match:
    selected_match = Int

    # The text line corresponding to the selected match:
    selected_line = Property # Int

    # The full name of the currently selected source file:
    selected_full_name = Property # File

    # The list of marked lines for the currently selected file:
    mark_lines = Property # List( Int )

    # Summary of current number of files and matches:
    summary = Property # Str

    #-- Traits UI Views --------------------------------------------------------

    view = View(
        VGroup(
            HGroup(
                Item( 'root',
                      id    = 'root',
                      label = 'Path',
                      width = 0.5
                ),
                Item( 'recursive' ),
                Item( 'file_type', label = 'Type' ),
                Item( 'search',
                      id     = 'search',
                      width  = 0.5,
                      editor = HistoryEditor( auto_set = True )
                ),
                Item( 'case_sensitive' )
            ),
            VSplit(
                VGroup(
                    Item( 'summary',
                          editor = TitleEditor()
                    ),
                    Item( 'source_files',
                          id     = 'source_files',
                          editor = table_editor
                    ),
                    dock        = 'horizontal',
                    show_labels = False
                ),
                VGroup(
                    HGroup(
                        Item( 'selected_full_name',
                              editor  = TitleEditor(),
                              springy = True
                        ),
                        Item( 'selected_full_name',
                              editor  = DNDEditor(),
                              tooltip = 'Drag this file'
                        ),
                        show_labels = False
                    ),
                    Item( 'selected_contents',
                          style  = 'readonly',
                          editor = CodeEditor( mark_lines    = 'mark_lines',
                                               line          = 'selected_line',
                                               selected_line = 'selected_line' )
                    ),
                    dock        = 'horizontal',
                    show_labels = False
                ),
                id = 'splitter'
            )
        ),
        title     = 'Live File Search',
        id        = 'enthought.developer.tools.file_search',
        width     = 0.75,
        height    = 0.67,
        resizable = True
    )

    #-- Property Implementations -----------------------------------------------

    @property_depends_on( 'search, case_sensitive' )
    def _get_filter ( self ):
        if len( self.search ) == 0:
            return lambda x: True

        return lambda x: len( x.matches ) > 0

    @property_depends_on( 'root, recursive, file_type' )
    def _get_source_files ( self ):
        root = self.root
        if root == '':
            root = getcwd()

        file_types = FileTypes[ self.file_type ]
        if self.recursive:
            result = []
            for dir_path, dir_names, file_names in walk( root ):
                for file_name in file_names:
                    if splitext( file_name )[1] in file_types:
                        result.append( SourceFile(
                            live_search = self,
                            full_name   = join( dir_path, file_name ) ) )
            return result

        return [ SourceFile( live_search = self,
                             full_name   = join( root, file_name ) )
                 for file_name in listdir( root )
                 if splitext( file_name )[1] in file_types ]

    @property_depends_on( 'selected' )
    def _get_selected_contents ( self ):
        if self.selected is None:
            return ''

        return ''.join( self.selected.contents )

    @property_depends_on( 'selected' )
    def _get_mark_lines ( self ):
        if self.selected is None:
            return []

        return [ int( match.split( ':', 1 )[0] )
                 for match in self.selected.matches ]

    @property_depends_on( 'selected, selected_match' )
    def _get_selected_line ( self ):
        selected = self.selected
        if (selected is None) or (len( selected.matches ) == 0):
            return 1

        return int( selected.matches[ self.selected_match - 1
                                    ].split( ':', 1 )[0] )

    @property_depends_on( 'selected' )
    def _get_selected_full_name ( self ):
        if self.selected is None:
            return ''

        return self.selected.full_name

    @property_depends_on( 'source_files, search, case_sensitive' )
    def _get_summary ( self ):
        source_files = self.source_files
        search       = self.search
        if search == '':
            return 'A total of %d files.' % len( source_files )

        files   = 0
        matches = 0
        for source_file in source_files:
            n = len( source_file.matches )
            if n > 0:
                files   += 1
                matches += n

        return 'A total of %d files with %d files containing %d matches.' % (
               len( source_files ), files, matches )

    #-- Traits Event Handlers --------------------------------------------------

    def _selected_changed ( self ):
        self.selected_match = 1

    def _source_files_changed ( self ):
        if len( self.source_files ) > 0:
            self.selected = self.source_files[0]
        else:
            self.selected = None

#-------------------------------------------------------------------------------
#  SourceFile class:
#-------------------------------------------------------------------------------

class SourceFile ( HasTraits ):

    # The search object this source file is associated with:
    live_search = Instance( FileSearch )

    # The full path and file name of the source file:
    full_name = File

    # The base file name of the source file:
    base_name = Property # Str

    # The portion of the file path beyond the root search path:
    ext_path = Property # Str

    # The contents of the source file:
    contents = Property # List( Str )

    # The list of matches for the current search criteria:
    matches = Property # List( Str )

    #-- Property Implementations -----------------------------------------------

    @property_depends_on( 'full_name' )
    def _get_base_name ( self ):
        return basename( self.full_name )

    @property_depends_on( 'full_name' )
    def _get_ext_path ( self ):
        return dirname( self.full_name )[ len( self.live_search.root ): ]

    @property_depends_on( 'full_name' )
    def _get_contents ( self ):
        try:
            fh = open( self.full_name, 'rb' )
            contents = fh.readlines()
            fh.close()
            return contents
        except:
            return ''

    @property_depends_on( 'full_name, live_search.[search, case_sensitive]' )
    def _get_matches ( self ):
        search = self.live_search.search
        if search == '':
            return []

        case_sensitive = self.live_search.case_sensitive
        if case_sensitive:
            return [ '%5d: %s' % ( (i + 1), line.strip() )
                     for i, line in enumerate( self.contents )
                     if line.find( search ) >= 0 ]

        search = search.lower()
        return [ '%5d: %s' % ( (i + 1), line.strip() )
                 for i, line in enumerate( self.contents )
                 if line.lower().find( search ) >= 0 ]

#-------------------------------------------------------------------------------
#  Run a stand-alone version of the tool if invoked from the command line:
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    FileSearch().configure_traits()

