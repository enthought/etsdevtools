#-------------------------------------------------------------------------------
#
#  Workbench views and perspectives for the objects in
#  etsdevtools.developer.tools.
#
#  Author: David C. Morrill
#          Vibha Srinivasan <vibha@enthought.com>
#
#  (c) Copyright 2006-2008 by Enthought, Inc.
#
#-------------------------------------------------------------------------------
# Imports
from pyface.workbench.api import TraitsUIView
from pyface.workbench.api import Perspective, PerspectiveItem
from etsdevtools.developer.tools.api import *

# Constants
ID = 'etsdevtools.developer.tools'

def get_universal_inspector_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.universal_inspector',
                obj = UniversalInspector(),
                name = 'Universal Inspector',
                window = window,
                **traits )

def get_object_source_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.object_source',
                obj = ObjectSource(),
                name = 'Object Source',
                window = window,
                **traits )

def get_class_browser_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.class_browser',
                obj = ClassBrowser(),
                name = 'Class Browser',
                window = window,
                **traits )

def get_favorites_browser_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.favorites_browser',
                obj = FavoritesBrowser(),
                name = 'Favorites Browser',
                window = window,
                **traits )

def get_ui_debugger_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.ui_debugger',
                obj  = UIDebugger(),
                name = 'UI Debugger',
                window = window,
                **traits )

def get_file_space_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.file_space',
                obj  = FileSpace(),
                name = 'File Space',
                window = window,
                **traits )

def get_file_browser_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.file_browser',
                obj  = FileBrowser(),
                name = 'File Browser',
                window = window,
                **traits )

def get_syntax_checker_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.syntax_checker',
                obj  = SyntaxChecker(),
                name = 'Syntax Checker',
                window = window,
                **traits  )

def get_view_tester_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.view_tester',
                obj  = ViewTester(),
                name = 'View Tester',
                window = window,
                **traits )

def get_traceback_viewer_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.traceback_viewer',
                obj  = TracebackViewer(),
                name = 'Traceback Viewer',
                window = window,
                **traits )

def get_fbi_viewer_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.fbi_viewer',
                obj  = FBIViewer(),
                name = 'FBI Viewer',
                window = window,
                **traits )

def get_traits_ui_db_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.traits_ui_db',
                obj  = TraitsUIDB(),
                name = 'Traits UI DB',
                window = window,
                **traits )

def get_app_monitor_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.app_monitor',
                obj  = AppMonitor(),
                name = 'Application Monitor',
                window = window,
                **traits )

def get_logger_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.logger',
                obj  = Logger(),
                name = 'Logger',
                window = window,
                **traits )

def get_wiretap_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.wiretap',
                obj  = Wiretap(),
                name = 'Wiretap',
                window = window,
                **traits )

def get_listener_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.listener',
                obj  = Listener(),
                name = 'Listener',
                window = window,
                **traits )

def get_object_viewer_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.object_viewer',
                obj  = ObjectViewer(),
                name = 'Object Viewer',
                window = window,
                **traits )

def get_browser_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.envisage_browser.browser',
                obj  = ApplicationBrowser(),
                name = 'Envisage Browser',
                window = window,
                **traits )

def get_profiler_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.profiler',
                obj  = Profiler(),
                name = 'Profiler',
                window = window,
                **traits)

def get_profile_viewer_view(window, **traits):
    return TraitsUIView(
                id   = ID + '.profile_viewer',
                obj  = ProfileViewer(),
                name = 'Profile Viewer',
                window = window,
                **traits)

def get_break_points_view(window, **traits):
    from etsdevtools.developer.helper.fbi import Breakpoints
    return TraitsUIView(
                id   = 'etsdevtools.developer.helper.fbi.break_points',
                obj  = Breakpoints(),
                name = 'Break Points',
                window = window,
                **traits)

def get_developer_perspective(**traits):
    return Perspective(
            id   = ID + '.perspective.developer',
            name = 'Developer Tools',
            show_editor_area = False,
            contents = [
                PerspectiveItem(
                    id       = ID + '.file_browser',
                    position = 'left',
                ),
                PerspectiveItem(
                    id       = ID + '.app_monitor',
                    position = 'right',
                )])

### EOF #######################################################################
