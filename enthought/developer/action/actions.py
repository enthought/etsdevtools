#-------------------------------------------------------------------------------
#  
#  Actions for the developer plugin.
#  
#  Author: David C. Morrill 
#          Vibha Srinivasan <vibha@enthought.com>
#  
#  (c) Copyright 2006-2008 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------
# Imports
from enthought.pyface.action.api import Action as PyfaceAction
from enthought.envisage.ui.workbench.api import \
    Workbench, WorkbenchActionSet
from enthought.envisage.ui.action.api \
    import Action, Group, Menu

# Constants
ID = 'enthought.developer'

class InvokeFBIAction(PyfaceAction):
    def perform(self, event):
        """ Performs the action. """
        from enthought.developer.helper.fbi import FBIInvoker
        FBIInvoker.invoke(event)

class RestoreBPAction(PyfaceAction):
    def perform(self, event):
        """ Performs the action. """
        from enthought.developer.helper.fbi import Breakpoints
        Breakpoints().restore()

def get_action_sets(**traits):
    workbench_action_set = WorkbenchActionSet(
    id   = ID + '.tools.workbench_action_set',
    name = 'Enthought developer tools plugins workbench actions',

    menus = [
        Menu( groups   = [ Group( id = 'enthought_developer_ToolsGroup') ],
              id       = 'enthought_developer_ToolsMenu',
              path = 'MenuBar',
              name     = 'Developer Tools',
              before = 'Help',
        ),
        Menu( groups   = [ Group( id = 'enthought_developer_DebugGroup' ) ],
              id       = 'enthought_developer_DebugMenu',
              path = 'MenuBar/enthought_developer_ToolsMenu',
              name     = 'Debug'
        ),
    ],
    actions = [
        Action( name        = 'Invoke FBI',
                tooltip     = 'Invoke the FBI debugger',
                class_name  = ID + '.action.actions.InvokeFBIAction',
                id          = 'enthought.developer.helper.fbi.fbi_invoker',
                path = 'MenuBar/enthought_developer_ToolsMenu/'
                               'enthought_developer_DebugMenu'
        ),
        Action( name        = 'Restore break points',
                tooltip     = 'Restores all previously saved break points',
                class_name  = ID + '.action.actions.RestoreBPAction',
                id          = 'enthought.developer.helper.fbi.break_points.restore',
                path = 'MenuBar/enthought_developer_ToolsMenu/'
                               'enthought_developer_DebugMenu'
        ),
    ]
)
    return workbench_action_set

### EOF #######################################################################