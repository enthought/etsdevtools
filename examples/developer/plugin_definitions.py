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

from os.path import abspath, dirname, join

import envisage
import envisage.plugins.python_shell

import etsdevtools.developer


#-------------------------------------------------------------------------------
#  Package locations:
#-------------------------------------------------------------------------------

envisage_path  = abspath(dirname(envisage.__file__))
developer_path = abspath(dirname(etsdevtools.developer.__file__))
pythonshell_path = abspath(dirname(envisage.plugins.python_shell.__file__))

#-------------------------------------------------------------------------------
#  The plugin definitions required by the application:
#-------------------------------------------------------------------------------

PLUGIN_DEFINITIONS = [
    # Envisage plugins:
    join(envisage_path, 'core/core_plugin_definition.py'),
    join(envisage_path, 'resource/resource_plugin_definition.py'),
    join(envisage_path, 'action/action_plugin_definition.py'),
    join(envisage_path, 'workbench/workbench_plugin_definition.py'),
    join(envisage_path, 'workbench/action/action_plugin_definition.py'),

    # Enthought plugins:
    join(pythonshell_path, 'python_shell_plugin_definition.py'),

    # Enthought developer tool plugins:
    join(developer_path, 'plugin_definition.py'),
    join(developer_path, 'fbi_plugin_definition.py'),
]

#-------------------------------------------------------------------------------
#  Plugin definitions that we want to import from but don't want as part of
#  the application:
#-------------------------------------------------------------------------------

INCLUDE = []
