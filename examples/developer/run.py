#-------------------------------------------------------------------------------
#  
#  Starts the Envisage environment.
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import sys

from enthought.envisage.ui.workbench.api import WorkbenchApplication
from enthought.envisage.core_plugin import CorePlugin    
from enthought.envisage.ui.workbench.workbench_plugin import \
         WorkbenchPlugin
from enthought.plugins.python_shell.python_shell_plugin import \
         PythonShellPlugin

# Enthought developer tool plugins:
from enthought.developer.developer_plugin import EnthoughtDeveloperPlugin
from enthought.developer.tools.fbi_plugin import FBIPlugin
from enthought.developer.helper.fbi \
    import enable_fbi
    
#-------------------------------------------------------------------------------
#  Application entry point:
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    
    # Allow the FBI to handle any exceptions that occur:
    enable_fbi()

    # Create an Envisage application:
    # FIXME: Including the FBIPlugin raises an error about the traits exception
    # notification handler being locked. This needs to be investigated.
    application = WorkbenchApplication(
        plugins = [CorePlugin(), WorkbenchPlugin(), PythonShellPlugin(),
                   EnthoughtDeveloperPlugin(), 
        #          FBIPlugin()
                   ],
        argv               = sys.argv,
        id                 = 'Enthought Developer Tools',
        requires_gui       = True
    )

    # Run the application
    application.run()