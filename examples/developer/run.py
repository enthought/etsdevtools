#-------------------------------------------------------------------------------
#  
#  Starts the Envisage environment.
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import sys

from enthought.envisage.api \
    import Application

from plugin_definitions \
    import INCLUDE, PLUGIN_DEFINITIONS

from enthought.developer.helper.fbi \
    import enable_fbi
    
#-------------------------------------------------------------------------------
#  Application entry point:
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    
    # Allow the FBI to handle any exceptions that occur:
    enable_fbi()
    
    # Create an Envisage application:
    application = Application(
        argv               = sys.argv,
        id                 = 'Enthought Developer Tools',
        include            = INCLUDE,
        plugin_definitions = PLUGIN_DEFINITIONS,
        requires_gui       = True
    )

    # Start the application (this call does not return until the GUI event
    # loop terminates):
    application.start()

    # Stop the application:
    application.stop()

