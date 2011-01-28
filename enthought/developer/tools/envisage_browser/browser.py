#-------------------------------------------------------------------------------
#
#  Envisage application structure browser.
#
#  Written by: David C. Morrill
#
#  Date: 06/17/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasTraits, Str, Instance, List, Enum, Property, Any, File

from enthought.traits.ui.api \
    import View, Tabbed, HSplit, VSplit, VGroup, HGroup, Item, TreeEditor, \
           EnumEditor, TableEditor, InstanceEditor, UIInfo, Handler

from enthought.traits.ui.tree_node \
    import TreeNode

from enthought.traits.ui.table_column \
    import ObjectColumn

from enthought.traits.ui.menu \
    import NoButtons

from enthought.developer.features.api \
    import DropFile

from enthought.developer.tools.envisage_browser.object_adapter_base \
    import ObjectAdapterBase

from enthought.developer.tools.envisage_browser.application_adapter \
    import ApplicationAdapter, ExtensionPointFileRefs, ExtensionPointRefs

from enthought.developer.tools.envisage_browser.plugin_definition_adapter \
    import PluginDefinitionAdapter, RequiredByAdapter, RequiresAdapter, \
           ExtensionPointsAdapter, ExtensionsAdapter

from enthought.developer.tools.envisage_browser.extension_point_adapter \
    import ExtensionPointAdapter, ExtensionPointClassAdapter

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# Map of query operator names to query method names:
OperatorMap = {
    '=':        '_query_equal',
    'contains': '_query_contains'
}

#-------------------------------------------------------------------------------
#  Browser query table editor definition:
#-------------------------------------------------------------------------------

query_table_editor = TableEditor(
    columns  = [ ObjectColumn( name = 'name' ),
                 ObjectColumn( name = 'file_name' ) ],
    selected = 'query_selected',
    editable = False
)

#-------------------------------------------------------------------------------
#  'BrowserNode' class:
#-------------------------------------------------------------------------------

class BrowserNode ( TreeNode ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Can the object's children be renamed?
    rename = True

    # Can the object's children be copied?
    copy = False

    # Can the object's children be deleted?
    delete = False

    # Can children be inserted (or just appended)?
    insert = False

#-------------------------------------------------------------------------------
#  Browser application tree editor definition:
#-------------------------------------------------------------------------------

application_tree_editor = TreeEditor(
    editable = False,
    selected = 'application_selected',
    nodes = [
        BrowserNode(
            node_for = [ ApplicationAdapter ],
            children = 'plugin_definitions_list',
            label    = '=Application'
        ),
        BrowserNode(
            node_for = [ PluginDefinitionAdapter ],
            children = 'nodes',
            label    = 'name'
        ),
        BrowserNode(
            node_for = [ RequiredByAdapter ],
            children = 'required_by',
            label    = '=Required By'
        ),
        BrowserNode(
            node_for = [ RequiresAdapter ],
            children = 'requires',
            label    = '=Requires'
        ),
        BrowserNode(
            node_for = [ ExtensionPointsAdapter ],
            children = 'extension_points',
            label    = '=Extension Points'
        ),
        BrowserNode(
            node_for = [ ExtensionsAdapter ],
            children = 'extensions',
            label    = '=Extensions'
        ),
        BrowserNode(
            node_for = [ ExtensionPointAdapter ],
            label    = 'name'
        ),
        BrowserNode(
            node_for = [ ExtensionPointClassAdapter ],
            label    = 'name'
        ),
    ]
)

#-------------------------------------------------------------------------------
#  Browser extension point tree editor definition:
#-------------------------------------------------------------------------------

extension_point_tree_editor = TreeEditor(
    editable = False,
    selected = 'extension_point_selected',
    nodes = [
        BrowserNode(
            node_for = [ ApplicationAdapter ],
            children = 'extension_points',
            label    = '=Extension Points'
        ),
        BrowserNode(
            node_for = [ ExtensionPointFileRefs ],
            children = 'file_refs',
            label    = 'name'
        ),
        BrowserNode(
            node_for = [ ExtensionPointRefs ],
            children = 'refs',
            label    = 'module_name'
        ),
        BrowserNode(
            node_for = [ ExtensionPointAdapter ],
            label    = 'name'
        ),
    ]
)

#-------------------------------------------------------------------------------
#  'ApplicationBrowser' class:
#-------------------------------------------------------------------------------

class ApplicationBrowser ( Handler ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The UIInfo object associated with the browser:
    info = Instance( UIInfo )

    # The name of the Envisage application file currently being viewed:
    file_name = File( drop_file = DropFile(
                          extensions = [ '.py' ],
                          tooltip    = 'Drop an Envisage application '
                                       'file here.' ) )

    # The Envisage ApplicationAdapter object being browsed:
    application_adapter = Instance( ApplicationAdapter )

    # The current selected application object being browsed:
    application_selected = Instance( HasTraits,
                                  connect = 'from:selected application object' )

    # The current selected extension point object being browsed:
    extension_point_selected = Instance( HasTraits,
                                  connect = 'from:selected extension point' )

    # Currently selected query result:
    query_selected = Any( connect = 'from:selected query result' )

    # The current query ExtensionPoint class name:
    query_extension_point = Str

    # The list of ExtensionPoint class names actually used:
    query_extension_points = Property

    # The current query trait name:
    query_trait_name = Str

    # The current list of possible trait names:
    query_trait_names = List

    # The current query operator:
    query_operator = Enum( 'contains', '=' )

    # The current query value:
    query_value = Str

    # The current set of query results:
    query_results = List

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Tabbed(
            VGroup(
                Item( 'application_adapter',
                      id         = 'application_1',
                      label      = 'Application Browser',
                      show_label = False,
                      editor     = application_tree_editor,
                      dock       = 'horizontal'
                ),
                label  = 'Application',
                dock   = 'tab',
                export = 'DockWindowShell'
            ),
            VGroup(
                Item( 'application_adapter',
                      id         = 'application_2',
                      label      = 'Extension Point Browser',
                      show_label = False,
                      editor     = extension_point_tree_editor,
                      dock       = 'horizontal'
                ),
                label  = 'Extension Points',
                dock   = 'tab',
                export = 'DockWindowShell'
            ),
            VGroup(
                HGroup(
                    Item( 'query_extension_point',
                          label  = 'Extension Point',
                          editor = EnumEditor(
                                       name = 'query_extension_points' )
                    ),
                    Item( 'query_trait_name',
                          label = 'Query',
                          editor = EnumEditor(
                                       name = 'query_trait_names' )
                    ),
                    Item( 'query_operator',
                          show_label = False ),
                    Item( 'query_value',
                          show_label = False ),
                    label       = 'Query Parameters',
                    show_border = True,
                    dock        = 'fixed'
                ),
                Item( 'query_results',
                      label      = 'Query Results',
                      show_label = False,
                      editor     = query_table_editor,
                      dock       = 'horizontal',
                ),
                label  = 'Query',
                dock   = 'tab',
                export = 'DockWindowShell'
            ),
            id = 'tabbed'
        ),
        id = 'enthought.developer.tools.envisage_browser.browser',
    )

#-- Handler Method Overrides ---------------------------------------------------

    def init_info ( self, info ):
        """ Informs the handler what the UIInfo object for a View will be.
        """
        self.info = info

#-- Property Implementations ---------------------------------------------------

    def _get_query_extension_points ( self ):
        if self.application_adapter is not None:
            return self.application_adapter.extension_point_names

        return []

#-- Event Handlers -------------------------------------------------------------

    def _file_name_changed ( self, file_name ):
        self.application_adapter = ApplicationAdapter( file_name = file_name )
        self.trait_property_changed( 'query_extension_points', [],
                                     self.query_extension_points )

    def _query_extension_point_changed ( self, name ):
        """ Handles the 'query_extension_point' trait being changed.
        """
        for epfr in self.application_adapter.extension_points:
            if name == epfr.name:
                break

        # Just get the first ExtensionPointAdapter:
        self._base_names  = base_names  = []
        self._other_names = other_names = []
        all_names = []
        epa       = epfr.file_refs[0].refs[0]
        names     = epa.names + [ 'name', 'file_name' ]
        for i, name in enumerate( names ):
            if name[:1] == '*':
                name = name[1:]
                if name not in all_names:
                    all_names.append( name )
                    other_names.append( name )
            elif name not in all_names:
                all_names.append( name )
                base_names.append( name )
        all_names.sort()
        self.query_trait_names = all_names
        if self.query_trait_name not in all_names:
            self.query_trait_name = 'file_name'
        self._do_query()

    def _query_trait_name_changed ( self ):
        """ Handles the 'query_trait_name' trait being changed.
        """
        self._do_query()

    def _query_operator_changed ( self ):
        """ Handles the 'query_operator' trait being changed.
        """
        self._do_query()

    def _query_value_changed ( self ):
        """ Handles the 'query_value' trait being changed.
        """
        self._do_query()

#-- Private Methods ------------------------------------------------------------

    def _do_query ( self ):
        """ Updates the 'query_results' based on the current set of 'query_xxx'
            values.
        """
        name = self.query_extension_point
        for epfr in self.application_adapter.extension_points:
            if name == epfr.name:
                break
        query_results = []
        query_name    = self.query_trait_name
        query_value   = self.query_value
        query_method  = getattr( self, OperatorMap[ self.query_operator ] )
        for file_ref in epfr.file_refs:
            for ep in file_ref.refs:
                if query_method( str( getattr( ep, query_name, '' ) ),
                                 query_value ):
                    query_results.append( ep )
        self.info.query_results.model.columns = [
            ObjectColumn( name = name ) for name in self._base_names ]
#        fixme: The following code is not actually supported by the TableEditor:
#        self.info.query_results.model.other_columns = [
#            ObjectColumn( name = name ) for name in self._other_names ]
        self.query_results = query_results
        if len( query_results ) > 0:
            self.query_selected = query_results[0]
        else:
            self.query_selected = None

    def _query_equal ( self, value1, value2 ):
        return (value1 == value2)

    def _query_contains ( self, value1, value2 ):
        return (value1.find( value2 ) >= 0)

#-------------------------------------------------------------------------------
#  Create export objects:
#-------------------------------------------------------------------------------

view = ApplicationBrowser()

