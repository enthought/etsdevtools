#-------------------------------------------------------------------------------
#
#  Plugin definitions.
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

import enthought.developer

import enthought.envisage

import enthought.plugins.python_shell

from os.path \
    import abspath, dirname, join

#-------------------------------------------------------------------------------
#  Package locations:
#-------------------------------------------------------------------------------

envisage  = abspath( dirname( enthought.envisage.__file__  ) )
developer = abspath( dirname( enthought.developer.__file__ ) )
pythonshell = abspath( dirname( enthought.plugins.python_shell.__file__ ) )

#-------------------------------------------------------------------------------
#  The plugin definitions required by the application:
#-------------------------------------------------------------------------------

PLUGIN_DEFINITIONS = [
    # Envisage plugins:
    join( envisage, 'core/core_plugin_definition.py' ),
    join( envisage, 'resource/resource_plugin_definition.py' ),
    join( envisage, 'action/action_plugin_definition.py' ),
    join( envisage, 'workbench/workbench_plugin_definition.py' ),
    join( envisage, 'workbench/action/action_plugin_definition.py' ),

    # Enthought plugins:
    join( pythonshell, 'python_shell_plugin_definition.py' ),

    # Enthought developer tool plugins:
    join( developer, 'plugin_definition.py' ),
    join( developer, 'fbi_plugin_definition.py' ),
]

#-------------------------------------------------------------------------------
#  Plugin definitions that we want to import from but don't want as part of
#  the application:
#-------------------------------------------------------------------------------

INCLUDE = []

