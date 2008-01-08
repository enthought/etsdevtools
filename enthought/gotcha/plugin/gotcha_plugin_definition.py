#-------------------------------------------------------------------------------
#  
#  The Gotcha! plugin.  
#  
#  Written by: David C. Morrill
#  
#  Date: 02/22/2005
#  
#  (c) Copyright 2005 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:  
#-------------------------------------------------------------------------------

from enthought.envisage.core.core_plugin_definition \
    import PluginDefinition, Preferences

from enthought.envisage.ui.ui_plugin_definition \
    import Action

from enthought.envisage.ui.ui_plugin_definition \
    import UIActions


# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = "enthought.gotcha.plugin"

#-------------------------------------------------------------------------------
#  Extensions:  
#-------------------------------------------------------------------------------

#-- Preferences ----------------------------------------------------------------

preferences = Preferences(
    defaults = {
        # Should the profiler cleanup all the profile files.
        'cleanup_profiles': True,
    }
)

#-- Actions --------------------------------------------------------------------

## new_viewer_action = Action(
##     id            = ID + ".actions.NewViewer",
##     class_name    = ID + ".actions.NewViewer",
##     name          = "Gotcha View",
##     description   = "Create a new Gotcha viewer window",
##     image         = "images/cpu_view.png",
##     tooltip       = "Create a new Gotcha viewer window",
##     tool_bar_path = "additions",
##     style         = "push",
## )
    
open_profile_action = Action(
    id            = ID + ".action.OpenProfile",
    class_name    = ID + ".action.OpenProfile",
    name          = "Open Profile",
    description   = "Open an existing Gotcha profile file",
    image         = "images/profile_open.png",
    tooltip       = "Open an existing Gotcha profile file",
    tool_bar_path = "additions",
    style         = "push",
)
    
begin_profiling_action = Action(
    id            = ID + ".action.BeginProfiling",
    class_name    = ID + ".action.BeginProfiling",
    name          = "Begin Profiling",
    description   = "Begin profiling",
    image         = "images/profile_start.png",
    tooltip       = "Begin profiling",
    tool_bar_path = "additions",
    style         = "push",
)
    
end_profiling_action = Action(
    id            = ID + ".action.EndProfiling",
    class_name    = ID + ".action.EndProfiling",
    name          = "End Profiling",
    description   = "End profiling",
    image         = "images/profile_stop.png",
    tooltip       = "End profiling",
    tool_bar_path = "additions",
    style         = "push",
)
    
ui_actions = UIActions(
    menus   = [],
    actions = [
##         new_viewer_action,
        open_profile_action,
        begin_profiling_action,
        end_profiling_action
    ]
)

#-------------------------------------------------------------------------------
#  The plugin definition:
#-------------------------------------------------------------------------------

PluginDefinition(
    # The plugin's globally unique identifier:
    id = ID,

    # The name of the class that implements the plugin:
    class_name = ID + ".gotcha_plugin.GotchaPlugin",

    # General information about the plugin:
    name          = "Gotcha Profiling Plugin",
    version       = "1.0.0",
    provider_name = "Enthought Inc",
    provider_url  = "www.enthought.com",
    autostart     = True,
    enabled       = True,

    # The Id's of the plugins that this plugin requires:
    requires = [
        "enthought.envisage.ui",
        "enthought.envisage.ui.preference"
    ],

    # The extension points offered by this plugin:
    extension_points = [],
    
    # The contributions that this plugin makes to extension points offered by
    # either itself or other plugins:
#   extensions = [ preferences, ui_actions ]
    extensions = [ ui_actions ]
)

