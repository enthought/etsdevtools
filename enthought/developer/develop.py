#-------------------------------------------------------------------------------
#  
#  Traits UI stand-alone developer environment
#  
#  Written by: David C. Morrill
#  
#  Date: 07/22/2007
#  
#  (c) Copyright 2007 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasTraits, HasPrivateTraits, Str, List, Instance, Button, Tuple, \
           Property, Dict, Enum, Bool, cached_property
    
from enthought.traits.ui.api \
    import View, VGroup, HGroup, Item, EnumEditor, ListEditor, Theme, spring, \
           UI, Handler, DNDEditor
           
from enthought.traits.ui.key_bindings \
    import KeyBindings, KeyBinding
    
from enthought.traits.ui.dock_window_theme \
    import white_dock_window_theme, white_bottom_dock_window_theme
    
from enthought.pyface.dock.features.api \
    import add_standard_features
    
from enthought.pyface.image_resource\
    import ImageResource
    
from helper.themes \
    import TButton, TText
    
from enthought.pyface.dock.dock_sizer \
    import DockImages
    
#-- The Tool Imports -----------------------------------------------------------

from enthought.developer.tools.app_monitor \
    import AppMonitor
    
from enthought.developer.tools.class_browser \
    import ClassBrowser
    
from enthought.developer.tools.favorites_browser \
    import FavoritesBrowser
    
from enthought.developer.tools.fbi_viewer \
    import FBIViewer
    
from enthought.developer.tools.file_browser \
    import FileBrowser
    
#from enthought.developer.tools.file_monitor \
#    import FileMonitor
    
from enthought.developer.tools.file_sieve \
    import FileSieve
    
from enthought.developer.tools.file_space \
    import FileSpace
    
from enthought.developer.tools.heap_browser \
    import HB_HeapBrowser
    
from enthought.developer.tools.image_browser \
    import ImageBrowser
    
from enthought.developer.tools.image_library_viewer \
    import ImageLibraryViewer
    
from enthought.developer.tools.image_theme_editor \
    import ImageThemeEditor
    
from enthought.developer.tools.listener \
    import Listener
    
from enthought.developer.tools.logger \
    import Logger
    
from enthought.developer.tools.log_file \
    import LogFile
    
from enthought.developer.tools.object_source \
    import ObjectSource
    
from enthought.developer.tools.object_viewer \
    import ObjectViewer
    
from enthought.developer.tools.profile_viewer \
    import ProfileViewer
    
from enthought.developer.tools.profiler \
    import Profiler
    
from enthought.developer.tools.syntax_checker \
    import SyntaxChecker
    
from enthought.developer.tools.traceback_viewer \
    import TracebackViewer
    
from enthought.developer.tools.traits_ui_db \
    import TraitsUIDB
    
from enthought.developer.tools.ui_debugger \
    import UIDebugger
    
from enthought.developer.tools.universal_inspector \
    import UniversalInspector
    
from enthought.developer.tools.view_tester \
    import ViewTester
    
from enthought.developer.tools.wiretap \
    import Wiretap
    
#from enthought.template.test.template_view \
#    import TemplateView
    
#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# The standard tools:
StdTools = {
    'Application Monitor':  AppMonitor,
    'Class Browser':        ClassBrowser,
    'Favorites Browser':    FavoritesBrowser,
    'FBI Viewer':           FBIViewer,
    'File Browser':         FileBrowser,
#   'File Monitor':         FileMonitor,
    'File Sieve':           FileSieve,
    'File Space':           FileSpace,
    'Heap Browser':         HB_HeapBrowser,
    'Image Browser':        ImageBrowser,
    'Image Library Viewer': ImageLibraryViewer,
    'Image Theme Editor':   ImageThemeEditor,
    'Listener':             Listener,
    'Logger':               Logger,
    'Log File':             LogFile,
    'Object Source':        ObjectSource,
    'Object Viewer':        ObjectViewer,
    'Profile Viewer':       ProfileViewer,
    'Profiler':             Profiler,
    'Syntax Checker':       SyntaxChecker,
    'Traceback Viewer':     TracebackViewer,
    'Traits UI DB':         TraitsUIDB,
    'UI Debugger':          UIDebugger,
    'Universal Inspector':  UniversalInspector,
    'View Tester':          ViewTester,
    'Wiretap':              Wiretap,
#    'Template View':       TemplateView
}

#-------------------------------------------------------------------------------
#  Key bindings tables:
#-------------------------------------------------------------------------------

tools_key_bindings = KeyBindings(
    KeyBinding( binding1 = 'Alt-t', method_name = '_select_next_tool',
                description = 'Selects the next tab on the current tools '
                              'page.' ),
    KeyBinding( binding1 = 'Alt-Shift-t', method_name = '_select_previous_tool',
                description = 'Selects the previous tab on the current tools '
                              'page.' )
)

pages_key_bindings = KeyBindings(
    KeyBinding( binding1 = 'Alt-p', method_name = '_select_next_page',
                description = 'Selects the next page tab.'),
    KeyBinding( binding1 = 'Alt-Shift-p', method_name = '_select_previous_page',
                description = 'Selects the previous page tab.' ),
    KeyBinding( binding1 = 'Alt-Shift-f', method_name = '_enable_fbi',
                description = 'Enables the FBI debugger.' )
)
    
#-------------------------------------------------------------------------------
#  'ToolsPage' class:
#-------------------------------------------------------------------------------

class ToolsPage ( HasPrivateTraits ):
    
    #-- Trait Definitions ------------------------------------------------------
    
    # The name of the page:
    name = Str
    
    # The list of tools on this page:
    tools = List( HasTraits )
    
    # The currently selected tool:
    selected = Instance( HasTraits )
    
    #-- Traits UI Views --------------------------------------------------------
    
    view = View(
        VGroup(
            Item( 'tools',
                  style  = 'custom',
                  editor = ListEditor( 
                               use_notebook = True,
                               deletable    = True,
                               dock_theme   = white_dock_window_theme,
                               dock_style   = 'tab',
                               export       = 'DockWindowShell',
                               page_name    = '.name',
                               selected     = 'selected' ) ),
            show_labels = False
        ),
        key_bindings = tools_key_bindings
    )
    
    #-- Commands ---------------------------------------------------------------
    
    def _select_next_tool ( self, info = None ):
        """ Selects the next tool tab.
        """
        self._select_tab( 1 )
    
    def _select_previous_tool ( self, info = None ):
        """ Selects the previous tool tab.
        """
        self._select_tab( -1 )
        
    #-- Private Methods --------------------------------------------------------
    
    def _select_tab ( self, delta ):
        """ Selects the next/previous tool tab.
        """
        tools = self.tools
        if len( tools ) > 1:
            try:
                index = tools.index( self.selected ) + delta
            except:
                index = 0
                
            self.selected = tools[ index % len( tools ) ]
    
#-------------------------------------------------------------------------------
#  'ToolsHandler' class:
#-------------------------------------------------------------------------------

class ToolsHandler ( Handler ):
    
    def init ( self, info ):
        """ Initializes the controls of a user interface.
        """
        info.object.ui = info.ui
    
#-------------------------------------------------------------------------------
#  'Tools' class:
#-------------------------------------------------------------------------------

class Tools ( HasPrivateTraits ):
    
    #-- Trait Definitions ------------------------------------------------------
    
    # Our traits UI object:
    ui = Instance( UI )
    
    # Optional test arguments when starting the test object's UI:
    test_args   = Tuple
    test_traits = Dict
    
    # The optional object being developed/tested:
    test_object = Instance( HasTraits )
    
    # The Traits UI object for the object being developed:
    test_ui = Instance( UI )
    
    # Mode in which to create a test object:
    create_as = Enum( 'Child', 'Independent', 'Tab' )
    
    # Can the test object be started now?  
    can_start = Property( depends_on = 'test_ui.control' )

    # The 'start' test object button:
    start_ui = Button( 'Start UI' )
    
    # List of active tools pages:
    pages = List( ToolsPage )
    
    # The current selected page:
    selected_page = Instance( ToolsPage )
    
    # The name of the current page:
    name = Str( 'Page' )
    
    # The list of available tools:
    tool_names = Property
    
    # The current selected tool name:
    selected_tool = Str( 'FBI Viewer' )
    
    # The 'add tool to active page' button:
    add_tool = Button( 'Add Tool' )
    
    # The 'create new page' button:
    new_page = Button( 'New Page' )
    
    # The 'Save active page' page button:
    save_page = Button( 'Save Page' )
    
    # The 'delete active page' button:
    delete_page = Button( 'Delete Page' )
    
    # Has the FBI been enabled yet?
    fbi_enabled = Bool( False )
    
    #-- Traits UI Views --------------------------------------------------------
    
    view = View(
        VGroup(
            HGroup(
                Item( 'create_as',
                      defined_when = 'test_object is not None' ),
                TButton( 'start_ui',
                      label        = 'Start UI',
                      #enabled_when = 'can_start',
                      defined_when = 'test_object is not None' ),
                '_',
                Item( 'test_object',
                      style        = 'readonly',
                      show_label   = False,
                      defined_when = 'test_object is not None',
                      tooltip      = 'Drag the application object',
                      editor = DNDEditor( image = ImageResource( 'object' ) ) ),
                Item( 'test_ui',
                      style        = 'readonly',
                      show_label   = False,
                      defined_when = 'test_object is not None',
                      enabled_when = 'test_ui is not None',
                      tooltip      = "Drag the application's Traits UI object",
                      editor = DNDEditor( image = ImageResource( 'ui' ),
                          disabled_image = ImageResource( 'disabled_ui' ) ) ),
                '_',
                spring,
                Item( 'selected_tool', 
                      show_label   = False,
                      editor       = EnumEditor( name = 'tool_names' ),
                      enabled_when = 'selected_page is not None' ),
                TButton( 'add_tool',
                      label        = 'Add Tool',
                      enabled_when = 'selected_page is not None' ),
                '_',
                TText( 'name' ),
                TButton( 'new_page',
                      label        = 'New Page',
                      enabled_when = "name.strip() != ''" ),
                TButton( 'save_page',
                      label        = 'Save Page',
                      enabled_when = 'selected_page is not None' ),
                TButton( 'delete_page',
                      label        = 'Delete Page',
                      enabled_when = 'selected_page is not None' ),
                group_theme = Theme( '@GFB', content = ( -7, -6 ) )
            ),
            VGroup(
                Item( 'pages',
                      style  = 'custom',
                      editor = ListEditor( 
                                   use_notebook = True,
                                   deletable    = True,
                                   dock_style   = 'tab',
                                   export       = 'DockWindowShell',
                                   page_name    = '.name',
                                   selected     = 'selected_page' ) ),
                show_labels = False,
                dock_theme  = white_bottom_dock_window_theme
            ),
            group_theme = '@XG2'
        ),
        title        = 'Enthought Developer Tools: Traits UI Edition',
        id           = 'enthought.developer.tools.Tools',
        width        = 0.75,
        height       = 0.75,
        resizable    = True,
        handler      = ToolsHandler,
        key_bindings = pages_key_bindings
    )
    
    #-- Property Implementations -----------------------------------------------
    
    @cached_property
    def _get_tool_names ( self ):
        names = StdTools.keys()
        names.sort()
        
        return names
        
    def _get_can_start ( self ):
        return ((self.test_ui is None) or (self.test_ui.control is None))
        
    #-- Trait Event Handlers ---------------------------------------------------
    
    def _start_ui_changed ( self ):
        """ Handles the 'Start UI' button being clicked.
        """
        if self.create_as == 'Tab':
            if self.selected_page is None:
                self._create_new_page()
            self.selected_page.tools.append( self.test_object )
        else:
            parent = None
            if self.create_as == 'Child':
                parent = self.ui.control
            self.test_traits[ 'parent' ] = parent
            self.test_ui = self.test_object.edit_traits( *self.test_args, 
                                                         **self.test_traits )
    
    def _selected_tool_changed ( self, tool ):
        """ Handles the selected tool being changed.
        """
        self._add_selected_tool()
        
    def _add_tool_changed ( self ):
        """ Handles the 'Add Tool' button being clicked.
        """
        self._add_selected_tool()
        
    def _new_page_changed ( self ):
        """ Handles the 'New Page' button being clicked.
        """
        self._create_new_page()
        
    def _save_page_changed ( self ):
        """ Handles the 'Save Page' button being clicked.
        """
        print 'Not implemented yet'
        
    def _delete_page ( self ):
        """ Handles the 'Delete Page' button being clicked.
        """
        self.pages.remove( self.selected_page )
        
    def _name_changed ( self, name ):
        """ Handles the selected page name being changed.
        """
        if self.selected_page is not None:
            name = name.strip()
            if name != '':
                self.selected_page.name = name
    
    #-- Commands ---------------------------------------------------------------
    
    def _select_next_page ( self, info = None ):
        """ Selects the next page tab.
        """
        self._select_tab( 1 )
    
    def _select_previous_page ( self, info = None ):
        """ Selects the previous page tab.
        """
        self._select_tab( -1 )
        
    def _enable_fbi ( self, info = None ):
        """ Enables the FBI debugger.
        """
        if not self.fbi_enabled:
            self.fbi_enabled = True
            
            from enthought.developer.helper.fbi import use_fbi
            use_fbi()
            
            print 'FBI Enabled'
        
    #-- Private Methods --------------------------------------------------------
    
    def _select_tab ( self, delta ):
        """ Selects the next/previous tool tab.
        """
        pages = self.pages
        if len( pages ) > 1:
            try:
                index = pages.index( self.selected_page ) + delta
            except:
                index = 0
                
            self.selected_page = pages[ index % len( pages ) ]
    
    def _create_new_page ( self ):
        """ Creates a new tools page.
        """
        page = ToolsPage( name = self.name )
        self.pages.append( page )
        self.selected_page = page

    def _add_selected_tool ( self ):
        """ Adds the currently selected tool as a new tool to the current page.
        """
        self.selected_page.tools.append( StdTools[ self.selected_tool ]() )
        
#-------------------------------------------------------------------------------
#  Factory for creating a standard, default Tools object:
#-------------------------------------------------------------------------------

def StandardTools ( ):
    """ Returns a standard, default Tools object.
    """
    # Make sure that all of the features have been added:
    add_standard_features()
    
    # Return a Tools object with one starter page containing a couple of tools:
    page  = ToolsPage( name  = 'Page', tools = [ UniversalInspector() ] )
    return Tools( pages = [ page ], selected_page = page )    
        
#-------------------------------------------------------------------------------
#  Helps a user develop a specified object or class:
#-------------------------------------------------------------------------------
                                
def develop ( obj_or_class, args = (), traits = {} ):
    """ Helps a user develop a specified object or class.
    """
    add_standard_features()
    page  = ToolsPage( name  = 'Develop', 
                       tools = [ UniversalInspector(), FBIViewer() ] )
    Tools( test_object   = obj_or_class,
           test_args     = args,
           test_traits   = traits,
           pages         = [ page ], 
           selected_page = page ).configure_traits()

#-- Run the program (if invoked from the command line) -------------------------

if __name__ == '__main__':
    StandardTools().configure_traits()
