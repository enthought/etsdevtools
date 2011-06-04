#-------------------------------------------------------------------------------
#
#  Extension point adapters for ExtensionPoint subclasses defined in:
#  - envisage.plugins.python_shell.python_shell_plugin_definition.py
#
#  Written by: David C. Morrill
#
#  Date: 06/18/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from traits.api \
    import HasPrivateTraits, Str, Property

from traitsui.api \
    import VSplit, Item, TableEditor

from traitsui.table_column \
    import ObjectColumn

from etsdevtools.developer.tools.envisage_browser.object_adapter \
    import Export

from etsdevtools.developer.tools.envisage_browser.extension_point_adapter \
    import ExtensionPointAdapter

#-------------------------------------------------------------------------------
#  Bindings table editor definition:
#-------------------------------------------------------------------------------

bindings_table_editor = TableEditor(
    columns  = [ ObjectColumn( name = 'name',  width = 0.20 ),
                 ObjectColumn( name = 'value', width = 0.77 ) ],
    editable = False
)

#-------------------------------------------------------------------------------
#  Commands table editor definition:
#-------------------------------------------------------------------------------

commands_table_editor = TableEditor(
    columns  = [ ObjectColumn( name = 'command', width = 0.97 ) ],
    editable = False
)

#-------------------------------------------------------------------------------
#  'NamespaceAdapter' class:
#-------------------------------------------------------------------------------

class NamespaceAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    bindings = Export
    commands = Export

    bindings_list = Property
    commands_list = Property

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VSplit(
                  Item( 'bindings_list~',
                        show_label = False,
                        dock       = 'tab',
                        editor     = bindings_table_editor
                  ),
                  Item( 'commands_list~',
                        show_label = False,
                        dock       = 'tab',
                        editor     = commands_table_editor
                  ),
                  id = 'splitter'
              )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ '*bindings', '*commands' ]

#-- Property Implementations ---------------------------------------------------

    def _get_bindings_list ( self ):
        if self._bindings_list is None:
            self._bindings_list = [ Binding( name = name, value = str( value ) )
                                    for name, value in self.bindings.items() ]
        return self._bindings_list

    def _get_commands_list ( self ):
        if self._commands_list is None:
            self._commands_list = [
                Command( command = command.replace( '\t', '    ' ) )
                for command in self.commands ]
        return self._commands_list

#-------------------------------------------------------------------------------
#  'Binding' class:
#-------------------------------------------------------------------------------

class Binding ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    name  = Str
    value = Str

#-------------------------------------------------------------------------------
#  'Command' class:
#-------------------------------------------------------------------------------

class Command ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    command = Str

