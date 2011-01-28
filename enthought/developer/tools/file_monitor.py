#-------------------------------------------------------------------------------
#
#  File Monitor plugin
#
#  Written by: David C. Morrill
#
#  Date: 08/10/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#  Notes:
#  - The syntax for a rule is:
#    [result=]package.module.function(arguments)
#
#    where:
#    - arguments = The arguments to be passed to the function, which can include
#      the following macro substitutions:
#      %n = The fully qualified name of the file the rule is being applied to.
#      %. = The fully qualified name of the file the rule is being applied to
#           minus the extension.
#      %p = The path of the file the rule is being applied to.
#      %r = The root of the file the rule is being applied to.
#      %x = The extension of the file the rule is being applied to.
#      %b = The base file the rule is being applied to (i.e. %r%x).
#      %c = The contents of the file the rule is being applied to.
#      %m = The Monitor object.
#      %^  = The base path being monitored.
#
#    - result = Optional description of the result being returned by the rule,
#               which can include any of the preceding macros. The value is used
#               as the name of the file that the result returned by the function
#               is written to. If omitted, the result is ignored.
#
#  Example:
#    enthought.developer.file_monitor.ftp( %n, %m, 'dmorrill.com', 'www' )
#
#------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import logging

from os.path \
    import abspath, split, splitext, isfile

from enthought.traits.api \
    import HasPrivateTraits, Str, List, Instance, Directory, Enum, true, \
           false

from enthought.traits.api \
    import View, Tabbed, VGroup, HGroup, Item, TableEditor, InstanceEditor

from enthought.developer.api \
    import read_file, truncate, import_symbol, file_watch


logger = logging.getLogger(__name__)


#-------------------------------------------------------------------------------
#  Trait definitions:
#-------------------------------------------------------------------------------

LogMode = Enum( 'Ignore', 'Print', 'Log' )

#-------------------------------------------------------------------------------
#  Returns the input arguments and keyword arguments:
#-------------------------------------------------------------------------------

def get_args ( *args, **kw ):
    """ Returns the input arguments and keyword arguments.
    """
    return ( args, kw )

#-------------------------------------------------------------------------------
#  'Rule' class:
#-------------------------------------------------------------------------------

class Rule ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The owner of the Rule:
    owner = Instance( 'FileMonitor' )

    # The name of the rule:
    name = Str

    # The file extension the rule applies to:
    extension = Str

    # The rule to be applied:
    rule = Str

    #---------------------------------------------------------------------------
    #  Applies the rule to a specified file for a specified Monitor:
    #---------------------------------------------------------------------------

    def apply ( self, file_name, monitor ):
        extension = self.extension.strip()
        if file_name[ -len( extension ): ] == extension:
            self.invoke( file_name, monitor )

    #---------------------------------------------------------------------------
    #  Invokes the rule for a specified file name for a specified Monitor:
    #---------------------------------------------------------------------------

    def invoke ( self, file_name, monitor ):
        """ Invokes the rule for a specified file name.
        """
        path, base = split( file_name )
        root, ext  = splitext( base )
        dic = {
            '%n': repr( file_name ),
            '%p': repr( path ),
            '%b': repr( base ),
            '%r': repr( root ),
            '%x': repr( ext ),
            '%^': repr( monitor.path ),
            '%.': repr( join( path, root ) ),
            '%m': 'monitor'
        }
        if '%c' in rule:
            dic[ '%c' ] = repr( read_file( file_name ) )

        monitor.invoke( file_name, self.substitute( rule, dic ) )

    #---------------------------------------------------------------------------
    #  Substitutes the various macros in a dictionary into a specified rule:
    #---------------------------------------------------------------------------

    def substitute ( self, rule, dic ):
        """ Substitutes the various macros in a dictionary into a specified rule.
        """
        for name, value in dic.items():
            rule = rule.replace( name, repr( value ) )

        return rule

#-------------------------------------------------------------------------------
#  'RuleSet' class:
#-------------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The owner of the RuleSet:
    owner = Instance( 'FileMonitor' )

    # The name of the rule set:
    name = Str

    # The set of rules:
    rules = List( Rule )

    #---------------------------------------------------------------------------
    #  Applies the rule set to a specified file for a specified Monitor:
    #---------------------------------------------------------------------------

    def apply ( self, file_name, monitor ):
        for rule in self.rules:
            rule.apply( file_name, monitor )

#-------------------------------------------------------------------------------
#  'Monitor' class:
#-------------------------------------------------------------------------------

class Monitor ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The owner of the Monitor:
    owner = Instance( 'FileMonitor' )

    # The path to be monitored:
    path = Directory

    # Should sub-directories be included?
    recursive = false

    # The rule set to apply to the monitored path:
    rule_set = Instance( RuleSet )

    # The set of available RuleSets:
    rule_sets = Property

    # Is the monitor enabled?
    enabled = true

    # Logging mode for information generated by rules:
    rule_log_mode = LogMode

    # Logging mode for information generated by rule processor functions:
    function_log_mode = LogMode

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        HGroup(
            Item( 'path',
                  width = -200
            ),
            Item( 'recursive',
                  label = 'Include subdirectories'
            ),
        ),
        HGroup(
            Item( 'rule_log_mode',
                  label = 'Log mode for rules'
            ),
            Item( 'function_log_mode',
                  label = 'Log mode for functions'
            )
        ),
        Item( 'rule_set',
              label = 'Rule Set',
              editor = InstanceEditor( name = 'rule_sets' ),
        ),
        Item( 'enabled' )
    )

    #---------------------------------------------------------------------------
    #  Activates the monitor:
    #---------------------------------------------------------------------------

    def activate ( self ):
        """ Activates the monitor.
        """
        if self.enabled:
            self.start_monitoring()

    #---------------------------------------------------------------------------
    #  Starts monitoring the associated path for file changes:
    #---------------------------------------------------------------------------

    def start_monitoring ( self ):
        """ Starts monitoring the associated path for file changes.
        """
        file_watch.watch( self._file_changed, self.path )

    #---------------------------------------------------------------------------
    #  Deactivates the monitor:
    #---------------------------------------------------------------------------

    def deactivate ( self ):
        """ Deactivates the monitor.
        """
        if self.enabled:
            self.stop_monitoring()

    #---------------------------------------------------------------------------
    #  Stops monitoring the associated path for file changes:
    #---------------------------------------------------------------------------

    def stop_monitoring ( self ):
        """ Stops monitoring the associated path for file changes.
        """
        file_watch.watch( self._file_changed, self.path, remove = True )

    #---------------------------------------------------------------------------
    #  Invokes a specified rule:
    #---------------------------------------------------------------------------

    def invoke ( self, file_name, rule ):
        """ Invokes a specified rule.
        """
        rlm = self.rule_log_mode
        self.log( "%s changed" % file_name, rlm )

        left = rule.find( '(' )
        if left < 0:
            self.log( 'Invalid syntax for rule:' % rule, rlm )
            return

        result = None
        equal  = rule.find( '=' )
        if equal >= 0:
            if equal < left:
                result = rule[: equal].strip()
                rule   = rule[ equal + 1: ].strip()
                left   = rule.find( '(' )
        function_name = rule[ : left ].strip()
        dot = function.find( '.' )
        if dot < 0:
            function_name = '%s.%s.%s' % ( self.owner.import_path,
                                           function_name, function_name )
        function = import_symbol( function_name )
        if function is None:
            self.log( 'Could not find function: ' + function_name, rlm )
            return

        params = rule[ left: ]
        try:
            args, kw = eval( 'get_args' + params )
        except:
            self.log( 'Syntax error in argument list: ' + params, rlm )
            return

        self.log( 'Applying rule: %s' % rule, rlm )

        data = function( *args, **kw )

        if (result is not None) and (data is not None):
            fh = None
            try:
                fh = file( result, 'wb' )
                fh.write( data )
                fh.close()
                self.log( 'Wrote result to: ' + result, rlm )
            except:
                self.log( 'Error writing result to: ' + result, rlm )
                if fh is not None:
                    try:
                        fh.close()
                    except:
                        pass

    #---------------------------------------------------------------------------
    #  Logs a specified message using a specified log mode:
    #---------------------------------------------------------------------------

    def log ( self, msg, log_mode = None ):
        """ Logs a specified message using a specified log mode.
        """
        if log_mode is None:
            log_mode = self.rule_log_mode

        if log_mode == 'Print':
            print msg

        elif log_mode == 'Log':
            logger.Info( msg )

    #---------------------------------------------------------------------------
    #  Handles the 'enabled' trait being changed:
    #---------------------------------------------------------------------------

    def _enabled_changed ( self, enabled ):
        """ Handles the 'enabled' trait being changed.
        """
        if enabled:
            self.start_monitoring()
        else:
            self.stop_monitoring()

    #---------------------------------------------------------------------------
    #  Handles a monitored file being changed:
    #---------------------------------------------------------------------------

    def _file_changed ( self, file_name ):
        """ Handles a monitored file being changed.
        """
        if isfile( file_name ):
            self.rule_set.apply( file_name, self )

    #---------------------------------------------------------------------------
    #  Implementation of the 'rule_sets' property:
    #---------------------------------------------------------------------------

    def _get_rule_sets ( self ):
        return self.owner.rule_sets

    #---------------------------------------------------------------------------
    #  Handles the 'owner' trait being changed:
    #---------------------------------------------------------------------------

    def _owner_changed ( self, old, new ):
        """ Handles the 'owner' trait being changed.
        """
        self.set_owner_listeners( old, True )
        self.set_owner_listeners( new, False )

    #---------------------------------------------------------------------------
    #  Sets/Resets the listeners on the object's 'owner':
    #---------------------------------------------------------------------------

    def set_owner_listeners ( self, object, remove ):
        """ Sets/Resets the listeners on the object's 'owner'.
        """
        if object is not None:
            object.on_trait_change( self._rule_sets_changed, 'rule_sets',
                                    remove = remove )
            object.on_trait_change( self._rule_sets_changed, 'rule_sets_items',
                                    remove = remove )

    #---------------------------------------------------------------------------
    #  Handles the owner's 'rule_sets' being changed:
    #---------------------------------------------------------------------------

    def _rule_sets_changed ( self ):
        """ Handles the owner's 'rule_sets' being changed.
        """
        self.trait_property_changed( 'rule_sets', [], self.rule_sets )

#-------------------------------------------------------------------------------
#  Defines the FileMonitor table editors:
#-------------------------------------------------------------------------------

monitor_table_editor = TableEditor(
)

rule_set_table_editor = TableEditor(
)

rules_table_editor = TableEditor(
)

#-------------------------------------------------------------------------------
#  'FileMonitor' plugin:
#-------------------------------------------------------------------------------

class FileMonitor ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'File Monitor' )

    # The persistence id for this object:
    id = Str( 'enthought.developer.tools.file_monitor.state',
              save_state_id = True )

    # The set of currently defined monitors:
    monitors = List( Monitor, save_state = True )

    # The set of currently defined rules sets:
    rule_sets = List( RuleSet, save_state = True )

    # The set of currently defined rules:
    rules = List( Rule, save_state = True )

    # Default path to import file monitor functions from:
    import_path = Str( 'enthought.developer.tools.file_monitor_functions',
                       save_state = True )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Tabbed(
            VGroup(
                Item( 'monitors',
                      show_label = False,
                      editor     = monitor_table_editor
                ),
                label = 'Monitors'
            ),
            VGroup(
                Item( 'rule_sets',
                      show_label = False,
                      editor     = rule_sets_table_editor
                ),
                label = 'Rule Sets'
            ),
            VGroup(
                Item( 'rules',
                      show_label = False,
                      editor     = rules_table_editor
                ),
                label = 'Rules'
            ),
            id = 'tabbed'
        )
    )

    options = View(
        Item( 'import_path',
              label = 'Default import path',
              width = -200
        ),
        id = 'enthought.developer.tools.file_monitor.options'
    )

    #---------------------------------------------------------------------------
    #  Handles the 'monitors' trait being changed:
    #---------------------------------------------------------------------------

    def _monitors_changed ( self, old, new ):
        """ Handles the 'monitors' trait being changed.
        """
        for monitor in old:
            monitor.owner = None
            monitor.activate()

        for monitor in new:
            monitor.owner = self
            monitor.deactivate()

    def _monitors_items_changed ( self, event ):
        for monitor in event.removed:
            monitor.owner = None
            monitor.deactivate()

        for monitor in event.added:
            monitor.owner = self
            monitor.activate()

    #---------------------------------------------------------------------------
    #  Handles the 'rule_sets' trait being changed:
    #---------------------------------------------------------------------------

    def _rule_sets_changed ( self, old, new ):
        """ Handles the 'rule_sets' trait being changed.
        """
        for rule_set in old:
            rule_set.owner = None

        for rule_set in new:
            rule_set.owner = self

    def _rule_sets_items_changed ( self, event ):
        """ Handles the 'rule_sets' trait being changed.
        """
        for rule_set in event.removed:
            rule_set.owner = None

        for rule_set in event.added:
            rule_set.owner = self

    #---------------------------------------------------------------------------
    #  Handles the 'rules' trait being changed:
    #---------------------------------------------------------------------------

    def _rules_changed ( self, old, new ):
        """ Handles the 'rules' trait being changed.
        """
        for rule in old:
            rule.owner = None

        for rule in new:
            rule.owner = self

    def _rules_items_changed ( self, event ):
        """ Handles the 'rules' trait being changed.
        """
        for rule in event.removed:
            rule.owner = None

        for rule in event.added:
            rule.owner = self

#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = FileMonitor()

