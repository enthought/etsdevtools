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

from envisage.api import Plugin
from traits.api import List
from pyface.dock.api import add_feature

# Local imports.
from view.views import *
from action.actions import get_action_sets
from features.api import DragDropFeature, DropFileFeature, ConnectFeature, \
     PopupMenuFeature, OptionsFeature, SaveStateFeature, SaveFeature, \
     ACustomFeature, DockControlFeature, DebugFeature

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# The plugin's globally unique identifier:
ID = 'enthought.developer.tools'

#-------------------------------------------------------------------------------
#  The test plugin:
#-------------------------------------------------------------------------------

class EnthoughtDeveloperPlugin( Plugin ):

    # Extension point Ids.
    VIEWS             = 'envisage.ui.workbench.views'
    PERSPECTIVES      = 'envisage.ui.workbench.perspectives'
    ACTION_SETS       = 'envisage.ui.workbench.action_sets'

    # The plugin's globally unique identifier:
    id = ID

    # General information about the plugin.
    name          = "Enthought Developer Tools Plugin"
    version       = "1.0.0"
    provider_name = "David C. Morrill"
    provider_url  = "www.enthought.com"

    # The views contributed by this plugin.
    views = List(contributes_to=VIEWS)

    # The perspectives contributed by this plugin.
    perspectives = List(contributes_to=PERSPECTIVES)

    # The action sets contributed by this plugin.
    action_sets = List(contributes_to=ACTION_SETS)

    #----------------------------------------------------------------------
    #  View definitions:
    #----------------------------------------------------------------------

    def _perspectives_default(self):
        return [get_developer_perspective]


    def _views_default(self):
        """ Traits initializer. """
        ## FIXME: We have omitted the envisage browser view from this list
        # since that code has not yet been upgraded to Envisage 3.
        return [get_universal_inspector_view,
                get_object_source_view, get_class_browser_view,
                get_favorites_browser_view, get_ui_debugger_view,
                get_file_space_view, get_file_browser_view,
                get_syntax_checker_view, get_view_tester_view,
                get_traceback_viewer_view, get_fbi_viewer_view,
                get_traits_ui_db_view, get_app_monitor_view, get_logger_view,
                get_wiretap_view, get_listener_view, get_object_viewer_view,
                get_profiler_view, get_profile_viewer_view, get_browser_view,
                get_break_points_view]

    def _action_sets_default(self):
        """ Traits initializer. """
        return [get_action_sets]

    def start(self):
         """ Start the plugin."""
         ## FIXME: In Envisage 2, Feature was an extension point declared in
         # envisage.ui.workbench, and this plugin offered extensions to
         # Feature. It looks like that support has not yet been included in
         # Envisage 3, and so, I am simply adding the features when the plugin
         # is started (instead of declaring an extension point here).

         for feature in [DragDropFeature,
                         DropFileFeature,
                         ConnectFeature,
                         PopupMenuFeature,
                         OptionsFeature,
                         SaveStateFeature,
                         SaveFeature,
                         ACustomFeature,
                         DockControlFeature,
                         DebugFeature]:
             add_feature(feature)

### EOF #######################################################################
