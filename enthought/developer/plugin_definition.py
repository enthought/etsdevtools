#-------------------------------------------------------------------------------
#
#  Sample plugin definition for the enthought.developer.tools and associated
#  DockWindow features.
#
#  Written by: David C. Morrill
#
#  Date: 06/25/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from envisage.core.core_plugin_definition \
    import PluginDefinition, ApplicationObject, Synchronizer

from envisage.workbench.workbench_plugin_definition \
    import Workbench, Perspective, View, Feature

from envisage.action.action_plugin_definition \
    import Action, Group, Location, Menu

from envisage.workbench.action.action_plugin_definition \
    import WorkbenchActionSet

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# The plugin's globally unique identifier:
ID = 'enthought.developer.tools'

#-------------------------------------------------------------------------------
#  View definitions:
#-------------------------------------------------------------------------------

views = [
    View( id   = 'enthought.developer.tools.universal_inspector',
          uol  = 'factory://enthought.developer.tools.universal_inspector.'
                 'UniversalInspector',
          name = 'Universal Inspector' ),
    View( id   = 'enthought.developer.tools.object_source',
          uol  = 'factory://enthought.developer.tools.object_source.ObjectSource',
          name = 'Object Source' ),
    View( id   = 'enthought.developer.tools.class_browser',
          uol  = 'import://enthought.developer.tools.class_browser.class_browser',
          name = 'Class Browser' ),
    View( id   = 'enthought.developer.tools.favorites_browser',
          uol  = 'factory://enthought.developer.tools.favorites_browser.'
                 'FavoritesBrowser',
          name = 'Favorites Browser' ),
    View( id   = 'enthought.developer.tools.ui_debugger',
          uol  = 'factory://enthought.developer.tools.ui_debugger.UIDebugger',
          name = 'UI Debugger' ),
    View( id   = 'enthought.developer.tools.file_space',
          uol  = 'factory://enthought.developer.tools.file_space.FileSpace',
          name = 'File Space' ),
    View( id   = 'enthought.developer.tools.file_browser',
          uol  = 'factory://enthought.developer.tools.file_browser.FileBrowser',
          name = 'File Browser' ),
    View( id   = 'enthought.developer.tools.syntax_checker',
          uol  = 'factory://enthought.developer.tools.syntax_checker.SyntaxChecker',
          name = 'Syntax Checker' ),
    View( id   = 'enthought.developer.tools.view_tester',
          uol  = 'factory://enthought.developer.tools.view_tester.ViewTester',
          name = 'View Tester' ),
    View( id   = 'enthought.developer.tools.traceback_viewer',
          uol  = 'factory://enthought.developer.tools.traceback_viewer.TracebackViewer',
          name = 'Traceback Viewer' ),
    View( id   = 'enthought.developer.tools.fbi_viewer',
          uol  = 'factory://enthought.developer.tools.fbi_viewer.FBIViewer',
          name = 'FBI Viewer' ),
    View( id   = 'enthought.developer.tools.traits_ui_db',
          uol  = 'factory://enthought.developer.tools.traits_ui_db.TraitsUIDB',
          name = 'Traits UI DB' ),
    View( id   = 'enthought.developer.tools.app_monitor',
          uol  = 'factory://enthought.developer.tools.app_monitor.AppMonitor',
          name = 'Application Monitor' ),
    View( id   = 'enthought.developer.tools.logger',
          uol  = 'factory://enthought.developer.tools.logger.Logger',
          name = 'Logger' ),
    View( id   = 'enthought.developer.tools.wiretap',
          uol  = 'factory://enthought.developer.tools.wiretap.Wiretap',
          name = 'Wiretap' ),
    View( id   = 'enthought.developer.tools.listener',
          uol  = 'factory://enthought.developer.tools.listener.Listener',
          name = 'Listener' ),
    View( id   = 'enthought.developer.tools.object_viewer',
          uol  = 'factory://enthought.developer.tools.object_viewer.ObjectViewer',
          name = 'Object Viewer' ),
    View( id   = 'enthought.developer.tools.envisage_browser.browser',
          uol  = 'factory://enthought.developer.tools.envisage_browser.browser.'
                 'ApplicationBrowser',
          name = 'Envisage Browser' ),
    View( id   = 'enthought.developer.tools.profiler',
          uol  = 'factory://enthought.developer.tools.profiler.Profiler',
          name = 'Profiler' ),
    View( id   = 'enthought.developer.tools.profile_viewer',
          uol  = 'factory://enthought.developer.tools.profile_viewer.ProfileViewer',
          name = 'Profile Viewer' ),
    View( id   = 'enthought.developer.helper.fbi.break_points',
          uol  = 'import://enthought.developer.helper.fbi.break_points',
          name = 'Break Points' ),
]

#-------------------------------------------------------------------------------
#  Workbench definition:
#-------------------------------------------------------------------------------

workbench = Workbench(

   perspectives = [
        Perspective(
            id   = ID + '.perspective.developer',
            name = 'Developer Tools',
            show_editor_area = False,
            contents = [
                Perspective.Item(
                    id       = 'enthought.developer.tools.file_browser',
                    position = 'left',
                ),
                Perspective.Item(
                    id       = 'enthought.developer.tools.app_monitor',
                    position = 'right',
                ),
            ]
        )
    ],

    views = views
)

#-------------------------------------------------------------------------------
#  Action set definitions:
#-------------------------------------------------------------------------------

workbench_action_set = WorkbenchActionSet(
    id   = ID + '.workbench_action_set',
    name = 'Enthought developer tools plugins workbench actions',

    groups = [
        Group( id       = 'enthought_developer_MenuBarGroup',
               location = Location( path   = 'MenuBar',
                                    before = 'HelpMenuGroup' )
        )
    ],

    menus = [
        Menu( groups   = [ Group( id = 'enthought_developer_ToolsGroup' ) ],
              id       = 'enthought_developer_ToolsMenu',
              location = Location(
                            path = 'MenuBar/enthought_developer_MenuBarGroup' ),
              name     = 'Developer Tools'
        ),
        Menu( groups   = [ Group( id = 'enthought_developer_DebugGroup' ) ],
              id       = 'enthought_developer_DebugMenu',
              location = Location(
                             path = 'MenuBar/enthought_developer_ToolsMenu/'
                                    'enthought_developer_ToolsGroup' ),
              name     = 'Debug'
        ),
    ],
    actions = [
        Action( name        = 'Invoke FBI',
                tooltip     = 'Invoke the FBI debugger',
                object      = 'import://enthought.developer.helper.fbi.FBIInvoker',
                method_name = 'invoke',
                id          = 'enthought.developer.helper.fbi.fbi_invoker',
                lazy_load   = True,
                locations   = [
                    Location(
                        path = 'MenuBar/enthought_developer_ToolsMenu/'
                               'enthought_developer_DebugMenu/'
                               'enthought_developer_DebugGroup'
                    )
                ],
        ),
        Action( name        = 'Restore break points',
                tooltip     = 'Restores all previously saved break points',
                object      = 'import://enthought.developer.helper.fbi.break_points',
                method_name = 'restore',
                id          = 'enthought.developer.helper.fbi.break_points.restore',
                lazy_load   = True,
                locations   = [
                    Location(
                        path = 'MenuBar/enthought_developer_ToolsMenu/'
                               'enthought_developer_DebugMenu/'
                               'enthought_developer_DebugGroup'
                    )
                ],
        ),
    ]
)

#-------------------------------------------------------------------------------
#  The test plugin definition:
#-------------------------------------------------------------------------------

class EnthoughtDeveloperPluginDefinition ( PluginDefinition ):

    # The plugin's globally unique identifier:
    id = ID

    # General information about the plugin.
    name          = "Enthought Developer Tools Plugin"
    version       = "1.0.0"
    provider_name = "David C. Morrill"
    provider_url  = "www.enthought.com"

    # The Ids of the plugins that this plugin requires:
    requires = [
        'envisage.core',
        'envisage.workbench'
    ]

    # The extension points offered by this plugin.
    extension_points = []

    # The contributions that this plugin makes:
    extensions = [
        workbench_action_set,
        workbench,

        Feature( class_name = 'enthought.developer.features.drag_drop_feature.'
                              'DragDropFeature' ),
        Feature( class_name = 'enthought.developer.features.drop_file_feature.'
                              'DropFileFeature' ),
        Feature( class_name = 'enthought.developer.features.connect_feature.'
                              'ConnectFeature' ),
        Feature( class_name = 'enthought.developer.features.popup_menu_feature.'
                              'PopupMenuFeature' ),
        Feature( class_name = 'enthought.developer.features.options_feature.'
                              'OptionsFeature' ),
        Feature( class_name = 'enthought.developer.features.save_state_feature.'
                              'SaveStateFeature' ),
        Feature( class_name = 'enthought.developer.features.save_feature.'
                              'SaveFeature' ),
        Feature( class_name = 'enthought.developer.features.custom_feature.'
                              'ACustomFeature' ),
        Feature( class_name = 'enthought.developer.features.dock_control_feature.'
                              'DockControlFeature' ),
        Feature( class_name = 'enthought.developer.features.debug_feature.'
                              'DebugFeature' ),
    ]

