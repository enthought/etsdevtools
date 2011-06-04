#------------------------------------------------------------------------------
#
#  Copyright (c) 2005, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#  Thanks for using Enthought open source!
#
#  Author: David C. Morrill
#  Date: 11/30/2004
#
#  Description: Envisage plugin definition for the Traits 'View Editing Tool'
#               (VET)
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from envisage.core.runtime.extension \
    import Plugin

from enthought_envisage_core_runtime \
    import Preferences

from enthought_envisage_ui \
    import Action, Group, Menu, UIActions, UIViews, View

from enthought_envisage_ui_preference \
    import PreferencePages, Page

#-------------------------------------------------------------------------------
#  Extensions:
#-------------------------------------------------------------------------------

#--- Preferences ---------------------------------------------------------------

preferences = Preferences(
    defaults = {
        'explode_on_exit': True,
    }
)

#--- Preference pages ----------------------------------------------------------

vet_preference_page = Page(
    id         = 'traits.vet.PreferencePage',
    class_name = 'traits.vet.PreferencePage',
    label      = 'VET Preferences',
    category   = '',
)

preference_pages = PreferencePages(
    pages = [ vet_preference_page ]
)

#--- Menus/Actions -------------------------------------------------------------

file_menu = Menu(
    id     = 'FileMenu',
    label  = 'File',
    path   = '',

    groups = [
        Group( name = 'AnExampleGroup' ),
        Group( name = 'AnotherGroup' ),
    ]
)

sub_menu = Menu(
    id     = 'SubMenu',
    label  = 'Sub',
    path   = 'FileMenu/AnExampleGroup',

    groups = [
        Group( name = 'MainGroup' ),
        Group( name = 'RadioGroup' ),
    ]
)

#do_it_action = Action(
#    id            = 'envisage.example.action.DoItAction',
#    class_name    = 'envisage.example.action.DoItAction',
#    label         = 'Do It!',
#    description   = "An action's description can appear in the status bar",
#    icon          = 'images/do_it.png',
#    tooltip       = 'A simple example action',
#    menu_bar_path = 'FileMenu/SubMenu/MainGroup',
#    tool_bar_path = 'additions',
#    style         = 'push',
#)
#
#higher_action = Action(
#    id            = 'envisage.example.action.HigherAction',
#    class_name    = 'envisage.example.action.DoItAction',
#    label         = 'Higher',
#    description   = "An action's description can appear in the status bar",
#    icon          = 'images/higher.png',
#    tooltip       = 'A simple example action',
#    menu_bar_path = 'FileMenu/SubMenu/RadioGroup',
#    tool_bar_path = 'RadioGroup',
#    style         = 'radio',
#)
#
#lower_action = Action(
#    id            = 'envisage.example.action.LowerAction',
#    class_name    = 'envisage.example.action.DoItAction',
#    label         = 'Lower',
#    description   = "An action's description can appear in the status bar",
#    icon          = 'images/lower.png',
#    tooltip       = 'A simple example action',
#    menu_bar_path = 'FileMenu/SubMenu/RadioGroup',
#    tool_bar_path = 'RadioGroup',
#    style         = 'radio',
#)
#
#overdrive_action = Action(
#    id            = 'envisage.example.action.OverdriveAction',
#    class_name    = 'envisage.example.action.DoItAction',
#    label         = 'Overdrive',
#    description   = "An action's description can appear in the status bar",
#    icon          = 'images/overdrive.png',
#    tooltip       = 'A simple example action',
#    menu_bar_path = 'FileMenu/SubMenu/',
#    tool_bar_path = 'additions',
#    style         = 'toggle',
#)
#
#ui_actions = UIActions(
#    menus   = [ file_menu, sub_menu ],
#    actions = [ do_it_action, higher_action, lower_action, overdrive_action ]
#)

#--- Views ---------------------------------------------------------------------

ui_views = UIViews(
    views = [
        View(
            name       = 'VET Edit View',
            icon       = 'images/stuff_view.png',
            id         = 'traits.vet.EditView',
            class_name = 'traits.vet.EditView',
            position   = 'left'
        ),
        View(
            name       = 'VET Visual View',
            icon       = 'images/stuff_view.png',
            id         = 'traits.vet.VisualView',
            class_name = 'traits.vet.VisualView',
            position   = 'top'
        ),
        View(
            name       = 'VET Property View',
            icon       = 'images/stuff_view.png',
            id         = 'traits.vet.PropertyView',
            class_name = 'traits.vet.PropertyView',
            position   = 'bottom'
        ),
    ]
)

#-------------------------------------------------------------------------------
#  Plugin definitions:
#-------------------------------------------------------------------------------

plugin = Plugin(
    # General information about the plugin:
    id            = 'traits.vet',
    name          = 'Traits View Editing Tool Plugin',
    version       = '1.0.0',
    provider_name = 'Enthought, Inc',
    provider_url  = 'www.enthought.com',
    autostart     = True,

    # The name of the class that implements the plugin:
    class_name = 'traits.vet.VETPlugin',

    # The Id's of the plugins that this plugin requires:
    requires = [
        'envisage.ui',
        'envisage.ui.preference',
        'envisage.ui.python_shell',
    ],

    # The extension points offered by this plugin to allow other plugins to
    # contribute to it:
    extension_points = [],

    # The contributions that this plugin makes to extension points offered by
    # other plugins:
    #extensions = [ ui_actions, ui_views, preferences, preference_pages ]
    extensions = [ ui_views, preferences, preference_pages ]
)

