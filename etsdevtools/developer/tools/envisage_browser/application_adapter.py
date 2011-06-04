#-------------------------------------------------------------------------------
#
#  Defines the ApplicationAdapter class which contains all of the top-level
#  information for defining a complete Envisage application needed by the
#  Envisage browser.
#
#  Written by: David C. Morrill
#
#  Date: 06/16/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import sys

from os.path \
    import abspath, split, splitext

from traits.api \
    import HasPrivateTraits, Str, File, List, Dict, Property

from traitsui.api \
    import View, VGroup, Tabbed, Item

from traitsui.menu \
    import NoButtons

from envisage.api import \
    Plugin

from etsdevtools.developer.tools.envisage_browser.object_adapter_base \
    import ObjectAdapterBase

from etsdevtools.developer.tools.envisage_browser.object_adapter \
    import ObjectAdapter

#-------------------------------------------------------------------------------
#  'ApplicationAdapter' class:
#-------------------------------------------------------------------------------

class ApplicationAdapter ( ObjectAdapterBase ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The dictionary mapping plugin ID's to PluginDefinitionAdapter objects:
    plugin_definitions = Dict

    # A list form of all of the plugin definitions:
    plugin_definitions_list = Property

    # A list of all extension points in the application:
    extension_points = Property

    # A list of all extension point names (in use):
    extension_point_names = Property

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View(
               Tabbed(
                   VGroup(
                       VGroup(
                           Item( 'file_name~' ),
                           label       = 'Implementation',
                           show_border = True
                       ),
                       label = 'Definition',
                       dock  = 'tab'
                   ),
                   VGroup(
                       Item( 'file_name~' ),
                       VGroup(
                           Item( 'source~', show_label = False )
                       ),
                       label = 'Source Code',
                       dock  = 'tab'
                   ),
                   id = 'tabbed'
               ),
               id        = 'etsdevtools.developer.tools.envisage_browser.'
                           'application_adapter.ApplicationAdapter',
               title     = 'Application Definition',
               resizable = True,
               buttons   = NoButtons
           )

#-- Public Methods -------------------------------------------------------------

    def get_plugins_using ( self, id ):
        """ Returns the list of all plugins using a specified plugin id.
        """
        return [ plugin for plugin in self.plugin_definitions_list
                 if id in plugin.requires ]

    def get_plugin_for ( self, id ):
        """ Returns an adapted plugin definition for the specified plugin id.
        """
        plugin = self.plugin_definitions.get( id )
        if plugin is not None:
            return plugin

        return UnknownPluginAdapter( id = id )

    def get_extension_for ( self, extension_point, file_name,
                                  container = None ):
        """ Returns an adapted extension point for the specified extension
            point object.
        """
        for klass in extension_point.__class__.__mro__:
            module_name = klass.__module__
            name   = ('etsdevtools.developer.tools.envisage_browser.' +
                      module_name.replace( '.', '_' ))
            module = self.import_module( name )
            if module is not None:
                adapter = getattr( module, klass.__name__ + 'Adapter', None )
                if adapter is not None:
                    try:
                        return adapter( adaptee     = extension_point,
                                        file_name   = file_name,
                                        application = self,
                                        container   = container )
                    except:
                        pass

        from extension_point_adapter import ExtensionPointAdapter
        return ExtensionPointAdapter( adaptee     = extension_point,
                                      file_name   = file_name,
                                      application = self,
                                      container   = container )

    def import_module_from_file ( self, file_name ):
        """ Imports a module from a specified file name.
        """
        file_name = abspath( file_name )
        for path in sys.path:
            path = abspath( path )
            n    = len( path )
            if ((len( file_name ) > (n + 1)) and
                (file_name[ : n ] == path)   and
                (file_name[n] in '/\\')):
                break
        else:
            path, file_name = split( file_name )
            sys.path.insert( 0, path )
            n = -1
        base, ext = splitext( file_name )
        name      = base[ n + 1: ].replace( '/', '.' ).replace( '\\', '.' )
        module    = self.import_module( name )
        if n < 0:
            del sys.path[0]
        return module

    def import_module ( self, name ):
        """ Imports and returns the module specified by 'name'.
        """
        try:
            module = __import__( name )
            for component in name.split( '.' )[1:]:
                module = getattr( module, component )

            return module
        except:
            return None

#-- Property Implementations ---------------------------------------------------

    def _get_plugin_definitions_list ( self ):
        if self._plugin_definitions_list is None:
            values = self.plugin_definitions.values()
            values.sort( lambda l, r: cmp( l.name, r.name ) )
            self._plugin_definitions_list = values

        return self._plugin_definitions_list

    def _get_extension_points ( self ):
        if self._extension_points is None:
            classes = {}

            for plugin in self.plugin_definitions_list:
                for ep in plugin.extension_points_all:
                    klass = ep.__class__
                    classes[ klass.__name__ ] = ( {}, plugin.file_name )

            for plugin in self.plugin_definitions_list:
                file_name   = plugin.file_name
                module_name = plugin.module.__name__
                for extension_point in plugin.adapted_extensions_all:
                    for klass in extension_point.base_classes:
                        refs = classes.get( klass.__name__ )
                        if refs is not None:
                            module_refs = refs[0].get( module_name )
                            if module_refs is None:
                                refs[0][ module_name ] = module_refs = \
                                    ( [], file_name )
                            module_refs[0].append( extension_point )

            eps = [ ExtensionPointFileRefs( name        = name,
                                            refs        = refs[0],
                                            file_name   = refs[1],
                                            application = self )
                    for name, refs in classes.items() if len( refs[0] ) > 0 ]
            eps.sort( lambda l, r: cmp( l.name, r.name ) )
            self._extension_points      = eps
            self._extension_point_names = [ epfr.name for epfr in eps ]

        return self._extension_points

    def _get_extension_point_names ( self ):
        if self._extension_point_names is None:
            self.extension_points

        return self._extension_point_names

#-- Event Handlers -------------------------------------------------------------

    def _file_name_changed ( self, file_name ):
        """ Handles the 'file_name' trait being changed.
        """
        app_module = self.import_module_from_file( file_name )
        if app_module is not None:
            names = dir(app_module)
            for name in names:
                item = getattr(app_module, name)
                object = None
                try:
                    if (issubclass( item, Plugin ) and
                         (item is not Plugin)):
                         object = item()
                         __import__(item.__module__)
                         plugin_module = sys.modules[item.__module__]
                except:
                    pass
                if object is not None:
                     self._plugin_definition( object, plugin_module )

#-- Private Methods ------------------------------------------------------------

    def _plugin_definition ( self, plugin, module ):
        """ Processes a plugin definition found within a specified module.
        """
        from etsdevtools.developer.tools.envisage_browser.plugin_definition_adapter \
             import PluginDefinitionAdapter

        self.plugin_definitions[ plugin.id ] = PluginDefinitionAdapter(
            adaptee     = plugin,
            module      = module,
            file_name   = self._module_file_name( module ),
            application = self )

    def _module_file_name ( self, module ):
        """ Returns the source file name for a specified module.
        """
        file_name = module.__file__
        base, ext = splitext( file_name )
        if ext == '.pyc':
            return base + '.py'

        return file_name

#-------------------------------------------------------------------------------
#  'ExtensionPointFileRefs' class:
#-------------------------------------------------------------------------------

class ExtensionPointFileRefs ( ObjectAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the extension point class:
    name = Str

    # The dictionary of ( file_name, extension points list ) pairs of all
    # extensions derived from this ExtensionPoint class:
    refs = Dict

    # List of ExtensionPointRefs derived from 'refs':
    file_refs = Property( List )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View(
               Tabbed(
                   VGroup(
                       VGroup(
                           Item( 'name~', label = 'Class Name' ),
                           label       = 'Description',
                           show_border = True
                       ),
                       VGroup(
                           Item( 'file_name~' ),
                           label       = 'Implementation',
                           show_border = True
                       ),
                       label = 'Definition',
                       dock  = 'tab'
                   ),
                   VGroup(
                       Item( 'file_name~' ),
                       VGroup(
                           Item( 'source~', show_label = False )
                       ),
                       label = 'Source Code',
                       dock  = 'tab'
                   ),
                   id = 'tabbed'
               ),
               id        = 'etsdevtools.developer.tools.envisage_browser.'
                           'application_adapter.ExtensionPointFileRefs',
               title     = 'Extension Point in File Definition',
               resizable = True,
               buttons   = NoButtons
           )

#-- Property Implementations ---------------------------------------------------

    def _get_file_refs ( self ):
        if self._file_refs is None:
            application = self.application
            refs = [ ExtensionPointRefs( module_name = module_name,
                                         refs        = refs[0],
                                         file_name   = refs[1],
                                         application = application )
                     for module_name, refs in self.refs.items() ]
            refs.sort( lambda l, r: cmp( l.module_name, r.module_name ) )
            self._file_refs = refs

        return self._file_refs

#-------------------------------------------------------------------------------
#  'ExtensionPointRefs' class:
#-------------------------------------------------------------------------------

class ExtensionPointRefs ( ObjectAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the module containing the Extension Point instances:
    module_name = Str

    # The list of extension points derived from this ExtensionPoint class:
    refs = List

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View(
               Tabbed(
                   VGroup(
                       VGroup(
                           Item( 'module_name~' ),
                           label       = 'Description',
                           show_border = True
                       ),
                       VGroup(
                           Item( 'file_name~' ),
                           label       = 'Implementation',
                           show_border = True
                       ),
                       label = 'Definition',
                       dock  = 'tab'
                   ),
                   VGroup(
                       Item( 'file_name~' ),
                       VGroup(
                           Item( 'source~', show_label = False )
                       ),
                       label = 'Source Code',
                       dock  = 'tab'
                   ),
                   id = 'tabbed'
               ),
               id        = 'etsdevtools.developer.tools.envisage_browser.'
                           'application_adapter.ExtensionPointRefs',
               title     = 'Extension Point Definition',
               resizable = True,
               buttons   = NoButtons
           )

#-------------------------------------------------------------------------------
#  'UnknownPluginAdapter' class:
#-------------------------------------------------------------------------------

class UnknownPluginAdapter ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The id of the unknown plugin:
    id = Str

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View(
               VGroup(
                   VGroup(
                       Item( 'id~', label = 'Name' ),
                       label       = 'Description',
                       show_border = True
                   ),
                   label = 'Definition',
                   dock  = 'tab'
               ),
               id        = 'etsdevtools.developer.tools.envisage_browser.'
                           'application_adapter.UnknownPluginAdapter',
               title     = 'Unknown Plugin Definition',
               resizable = True,
               buttons   = NoButtons
           )

